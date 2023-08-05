# -*- coding: utf-8 -*-
"""
This module allows to evaluate, compare and aggregate putative Gene Regulatory
Networks, using `scikit-learn`_.

.. _scikit-learn:
    https://scikit-learn.org
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import networkx as nx
from grenadine.Inference.inference import rank_GRN,clean_nan_inf_scores
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from tqdm import tqdm

__author__ = "Sergio Peignier, Pauline Schmitt"
__copyright__ = "Copyright 2019, The GReNaDIne Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"


def jaccard_similarity(joined_ranks, k):
    """
    Compute the Jaccard similarity between GRN inference methods.

    Args:
        joined_ranks (pandas.DataFrame): joined ranks for different methods,
            where rows represent possible regulatory links, and columns
            represent each method. The value at row i and column j represents
            the rank or the score of edge i computed by method j.
        k (int): Top k number of top ranked links to be compared

    Returns:
        pandas.DataFrame: Square matrix with GRNI methods Jaccard similaties
            Value at row i and column j represents the Jaccard similarity
            between the top k edges found by methods i and j resp.

    Example:
        >>> import pandas as pd
        >>> joined_ranks = pd.DataFrame([[1, 1, 2],[2, 2, 3],[3, 3, 1]],
                                        columns=['method1','method2','method3'],
                                        index=['gene1_gene2',
                                               'gene1_gene3',
                                               'gene3_gene2'])
        >>> joined_ranks
                     method1  method2  method3
        gene1_gene2        1        1        2
        gene1_gene3        2        2        3
        gene3_gene2        3        3        1
        >>> similarity = jaccard_similarity(joined_ranks,2)
        >>> similarity
                  method1   method2   method3
        method1       NaN         1  0.333333
        method2         1       NaN  0.333333
        method3  0.333333  0.333333       NaN

    """
    jaccard_sim = pd.DataFrame(columns=joined_ranks.columns,
                               index=joined_ranks.columns)
    methods = list(jaccard_sim.columns)
    for i,c in enumerate(methods[:-1]):
        top_k_c = list(joined_ranks[c].sort_values().index)[:k]
        for j,b in enumerate(methods[i+1:]):
            top_k_i = list(joined_ranks[b].sort_values().index)[:k]
            inter = len(set(top_k_i).intersection(set(top_k_c)))
            union = len(set(top_k_i).union(set(top_k_c)))
            jaccard_sim.loc[b,c] = inter/union
            jaccard_sim.loc[c,b] = jaccard_sim.loc[b,c]
    return(jaccard_sim)

def get_top_k_edges(method_ranks,k):
    """
    Return the top k edges for a given method.

    Args:
        method_ranks (pandas.Series): edges ranks for a given method, where each
            element represents the rank of a given edge
        k (int): top k edges to select

    Returns:
        list: list of the top k edges

    Example:
        >>> import pandas as pd
        >>> method_ranks = pd.Series([1,4,2,3], index=['gene1_gene2',
                                                       'gene1_gene3',
                                                       'gene3_gene1',
                                                       'gene3_gene2'])
        >>> edges = get_top_k_edges(method_ranks,2)
        >>> edges
        ['gene1_gene2', 'gene3_gene1']

    """
    return list(method_ranks.sort_values().index)[:k]

def get_top_k_edges_per_node(method_ranks,k,tg=1):
    """
    Return the top k edges per node.

    Args:
        method_ranks (pandas.Series): edges ranks for a given method, where each
            element represents the rank of a given edge
        k (int): top k edges to select
        tg (bool): True for TGs and False for TFs

    Returns:
        list: list of top k edges

    Example:
        >>> import pandas as pd
        >>> method_ranks = pd.Series([1,4,2,3], index=['gene1_gene2',
                                                       'gene1_gene3',
                                                       'gene3_gene1',
                                                       'gene3_gene2'])
        >>> # Top 1 edges per target gene
        >>> get_top_k_edges_per_node(method_ranks,1)
        ['gene1_gene2', 'gene1_gene3', 'gene3_gene1']
        >>> # Top 1 edges per transcription factor
        >>> get_top_k_edges_per_node(method_ranks,1,tg=0)
        ['gene1_gene2', 'gene3_gene1']

    """
    get_tg = lambda x: x.split("_")[int(tg)]
    tg = method_ranks.index.map(get_tg)
    gb = method_ranks.groupby(tg)
    top_k_edges_per_tg_list = gb.apply(get_top_k_edges,k)
    top_k_edges_per_tg = []
    for g in tg:
        top_k_edges_per_tg += top_k_edges_per_tg_list[g]
    top_k_edges_per_tg = np.unique(top_k_edges_per_tg)
    return list(top_k_edges_per_tg)


def union_top_k_edges(joined_ranks,
                      k,
                      method_selection=get_top_k_edges,
                      **method_selection_args):
    """
    Compute the top k edges found by different GRN inference methods.

    Args:
        joined_ranks (pandas.DataFrame): joined ranks for different methods,
            where rows represent possible regulatory links, and columns
            represent each method. The value at row i and column j represents
            the rank or the score of edge i computed by method j.
        k (int): Top k number of top ranked links to be compared
        method_selection (function): Method used to select top k edges for
            each algorithm (e.g., top k, top k for each tg, top k for each tf)
            this function should receive as parameters a pandas.Series of ranks
            and k.
    Returns:
        list: union of the top k edges of the different methods

    Example:
        >>> import pandas as pd
        >>> from grenadine.Evaluation.evaluation import get_top_k_edges
        >>> joined_ranks = pd.DataFrame([[1,1,2],[2,2,3],[4,3,1],[3,4,4]],
                                        columns=['method1',
                                                 'method2',
                                                 'method3'],
                                        index=['gene1_gene2',
                                               'gene1_gene3',
                                               'gene3_gene2',
                                               'gene3_gene1'])
        >>> joined_ranks
                     method1  method2  method3
        gene1_gene2        1        1        2
        gene1_gene3        2        2        3
        gene3_gene2        4        3        1
        gene3_gene1        3        4        4
        >>> union_top_k_edges(joined_ranks, k=2, method_selection=get_top_k_edges)
        ['gene1_gene3', 'gene1_gene2', 'gene3_gene2']
        >>> union_top_k_edges(joined_ranks, k=1, method_selection=get_top_k_edges)
        ['gene1_gene2', 'gene3_gene2']

    """
    union_top_k = set()
    for i,c in enumerate(joined_ranks):
        top_k_c = method_selection(joined_ranks[c],k,**method_selection_args)
        union_top_k = union_top_k.union(set(top_k_c))
    return(list(union_top_k))

def score_top_k_edges(joined_ranks,
                      k,
                      method_selection=get_top_k_edges,
                      **method_selection_args):
    """
    Compute the number of methods that find each edge.

    Args:
        joined_ranks (pandas.DataFrame): joined ranks for different methods,
            where rows represent possible regulatory links, and columns
            represent each method. The value at row i and column j represents
            the rank or the score of edge i computed by method j.
        k (int): Top k number of top ranked links to be compared
        method_selection (function): Method used to select top k edges for
            each algorithm (e.g., top k, top k for each tg, top k for each tf)
            this function should receive as parameters a pandas.Series of ranks
            and k.
    Returns:
        pandas.Series: number of methods having detected each edge

    Example:
        >>> import pandas as pd
        >>> from grenadine.Evaluation.evaluation import get_top_k_edges
        >>> joined_ranks = pd.DataFrame([[1,1,2],[2,2,3],[4,3,1],[3,4,4]],
                                        columns=['method1',
                                                 'method2',
                                                 'method3'],
                                        index=['gene1_gene2',
                                               'gene1_gene3',
                                               'gene3_gene2',
                                               'gene3_gene1'])
        >>> score_top_k_edges(joined_ranks, k=2, method_selection=get_top_k_edges)
        gene1_gene2    3
        gene1_gene3    2
        gene3_gene2    1
        gene3_gene1    0
        >>> score_top_k_edges(joined_ranks, k=1, method_selection=get_top_k_edges)
        gene1_gene2    2
        gene1_gene3    0
        gene3_gene2    1
        gene3_gene1    0

    """
    union_top_k = pd.Series(0,index = joined_ranks.index)
    for i,c in enumerate(joined_ranks):
        top_k_c = method_selection(joined_ranks[c],k,**method_selection_args)
        union_top_k[top_k_c] += 1
    return(union_top_k)

def pca_representation(joined_ranks,k,**pca_parameters):
    """
    Map the method to the space of the union of top k edges and apply PCA.

    Args:
        joined_ranks (pandas.DataFrame): joined ranks for different methods,
            where rows represent possible regulatory links, and columns
            represent each method. The value at row i and column j represents
            the rank or the score of edge i computed by method j.
        k (int): Top k number of top ranked links to be compared
        pca_parameters: Named parameter for the sklearn PCA method

    Returns:
        pandas.DataFrame: methods coordinates along principal components, where
        rows represent methods and columns representt Principal Components.

    Example:
        >>> import pandas as pd
        >>> joined_ranks = pd.DataFrame([[1,1,2],[2,2,3],[4,3,1],[3,4,4]],
                                        columns=['method1',
                                                 'method2',
                                                 'method3'],
                                        index=['gene1_gene2',
                                               'gene1_gene3',
                                               'gene3_gene2',
                                               'gene3_gene1'])
        >>> pca = pca_representation(joined_ranks, k=2)
        [9.81125224e-01 1.88747757e-02 1.60366056e-32]
        >>> pca
                        0         1             2
        method1 -1.400804 -0.194292  1.790900e-16
        method2 -0.512730  0.265408  1.790900e-16
        method3  1.913533 -0.071116  1.790900e-16

    """
    # Select only edges that are in the top k of at least one method
    edges = union_top_k_edges(joined_ranks,k)
    rankings = joined_ranks.loc[edges]
    # transpose the rankings
    rankingsT = rankings.T
    # create PCA object
    pca = PCA(**pca_parameters)
    # Apply the PCA
    rankingsT_pca = pca.fit_transform(rankingsT)
    rankingsT_pca = pd.DataFrame(rankingsT_pca)
    rankingsT_pca.index = rankingsT.index
    print(pca.explained_variance_ratio_)
    return(rankingsT_pca)

def edges2boolvec(total_edges, chosen_edges):
    """
    Build a boolean vector from a list of edges.

    Args:
        total_edges (list or numpy.array): total list of edges to be considered.
            Each element of the output boolean vector represents each link from
            this list
        chosen_edges (list or numpy.array): list of edges to be labeled as 1s

    Returns:
        pandas.Series: boolean list representing edges received as parameters.
            Each element of the output boolean vector represents each link from
            total_edges list, and the corresponding value is equal to 1 if the
            edge is also in chosen_edges and 0 otherwise

    Example:
        >>> edges = ['gene1_gene2', 'gene1_gene3', 'gene3_gene2', 'gene3_gene1']
        >>> chosen_edges = ['gene1_gene2','gene3_gene1']
        >>> edges2boolvec(edges, chosen_edges)
        gene1_gene2    1
        gene1_gene3    0
        gene3_gene2    0
        gene3_gene1    1

    """
    #print(np.asarray([e in total_edges for e in chosen_edges]).all())
    y = pd.Series(0,index=total_edges)
    y[chosen_edges] = 1
    return(y)

def KneeLocator(fpr, tpr):
    """
    Find the optimal ROC curve point (closest to (0,1)).

    Args:
        fpr (numpy.array): false positive rate array
        tpr (numpy.array): true positive rate array

    Returns:
        int: optimal point index

    Example:
        >>> import numpy as np
        >>> import pandas as pd
        >>> np.random.seed(0)
        >>> fpr = np.sort(np.random.rand(10))
        >>> np.random.seed(1)
        >>> tpr = np.sort(np.random.rand(10))
        >>> index = KneeLocator(fpr, tpr)
        >>> print("Optimal ROC point is ( fpr =", fpr[index], "; tpr =", tpr[index], ")")
        Optimal ROC point is ( fpr = 0.3834415188257777 ; tpr = 0.538816734003357 )

    """
    distances = np.sqrt((fpr**2 + (tpr-1)**2))
    i = np.argmin(distances)
    return i

def get_y_targets(gold_std_grn, scores=None, ranks=None, n_links=100000):
    """
    Get ground truth and predictor's estimation of a GRN, in a format ready to
    be used in sklearn.metrics functions.

    Args:
        scores (pandas.DataFrame): co-expression score matrix, where rows are
            target genes and columns are transcription factors.
            The value at row i and column j represents the score assigned by a
            score_predictor to the regulatory relationship between target gene i
            and transcription factor j.
        ranks (pandas.DataFrame): ranking matrix. A ranking matrix contains a
            row for each possible regulatory link, it also contains 4 columns,
            namely the rank, the score, the transcription factor id, and the
            target gene id.
        gold_std_grn (pandas.DataFrame): reference GRN used as a gold standard,
            where rows are links with index of the type <TF symbol>_<TG symbol>,
            and columns are respectively 'TF':TF symbol, 'TG':TG symbol, and
            'IS_REGULATED': indicates whether the link exists (1) or not (0)
        n_links (int): number of highest scores to keep from the
            estimated scores matrix

    Returns:
        (pandas.Series, pandas.Series, pandas.Series): tuple containing:

             (y_true, y_pred, y_pred_binary). y_true, boolean values for the
             ground truth (correct target values) of the GRN.
             y_pred, continuous values of the estimated GRN.
             y_pred_binary, boolean values of the estimated GRN, found by
             computing the argmin of the euclidean distance to the optimal roc
             curve point (0,1)

    Examples:
        >>> import pandas as pd
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> scores = pd.DataFrame(np.random.randn(3, 2),
                                  index=["gene1", "gene2", "gene3"],
                                  columns=["gene1", "gene3"])
        >>> # scores associated to self loops are set to nan
        >>> scores.iloc[0,0]=np.nan
        >>> scores.iloc[2,1]=np.nan
        >>> scores
                  gene1     gene3
        gene1       NaN  0.400157
        gene2  0.978738  2.240893
        gene3  1.867558       NaN
        >>> grn = pd.DataFrame(np.array([['gene1', 'gene2', 1],
                                         ['gene1', 'gene3', 0],
                                         ['gene3', 'gene2', 1],
                                         ['gene3', 'gene1', 0]]),
                                         columns=['TF', 'TG', 'IS_REGULATED'])
        >>> grn.index=grn['TF']+'_'+grn['TG']
        >>> grn["IS_REGULATED"] = grn["IS_REGULATED"].astype(int)
        >>> grn
                        TF     TG  IS_REGULATED
        gene1_gene2  gene1  gene2             1
        gene1_gene3  gene1  gene3             0
        gene3_gene2  gene3  gene2             1
        gene3_gene1  gene3  gene1             0
        >>> y_true, y_pred, y_pred_binary = get_y_targets(scores, grn, n_links=3)
        >>> y_true
        gene1_gene3    0
        gene1_gene2    1
        gene3_gene2    1
        >>> y_pred
        gene1_gene3    1.867558
        gene1_gene2    0.978738
        gene3_gene2    2.240893
        >>> y_pred_binary
        gene1_gene3    0
        gene1_gene2    0
        gene3_gene2    1

    """
    if scores is None and ranks is None:
        return None
    if scores is not None and ranks is None:
        scores = clean_nan_inf_scores(scores)
        ranks = rank_GRN(coexpression_scores_matrix=scores,take_abs_score=False)
    ranks_top = ranks.iloc[:n_links,:] # taking only n_links best links
    mutual_edges = set(ranks_top.index).intersection(set(gold_std_grn.index)) # taking links that are both in ranks_top and in the golden standard
    if not len(mutual_edges):
        print("Warning: no common edges between gold standard and top-k predicted links")
        return(None,None,None)
    # Amongst n_links best links, we select the ones that are in the golden standard
    ranks_top_in_golden = ranks_top.loc[mutual_edges]
    # Amongst links in the golden standard, we select the ones that appear in the n_links best links
    golden = gold_std_grn.loc[mutual_edges]

    y_pred = ranks_top_in_golden["score"]
    y_true = golden["IS_REGULATED"]
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    i = KneeLocator(fpr, tpr)
    thr = thresholds[i]
    y_pred_binary = np.zeros(y_pred.shape)
    y_pred_binary[y_pred >= thr] = 1
    y_pred_binary = pd.Series(y_pred_binary.astype(int))
    y_pred_binary.index = y_pred.index
    return y_true, y_pred, y_pred_binary


def evaluate_result(scores, gold_std_grn, n_links=100000):
    """
    Evaluate the performance of a GRN predictor based on the estimated scores,
    compared with the gold standard. Uses metrics from `scikit-learn`_.

    Args:
        scores (pandas.DataFrame): co-expression score matrix, where rows are
            target genes and columns are transcription factors.
            The value at row i and column j represents the score assigned by a
            score_predictor to the regulatory relationship between target gene i
            and transcription factor j.
        gold_std_grn (pandas.DataFrame): reference GRN used as a gold standard,
            where rows are links with index of the type <TF symbol>_<TG symbol>,
            and columns are respectively 'TF':TF symbol, 'TG':TG symbol, and
            'IS_REGULATED': indicates whether the link exists (1) or not (0)
        n_links (int): number of highest scores to keep from the estimated
            scores matrix

    Returns:
        pandas.Series: values of evaluation metrics for the estimated GRN

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> scores = pd.DataFrame(np.random.randn(3, 2),
                                  index=["gene1", "gene2", "gene3"],
                                  columns=["gene1", "gene3"])
        >>> # scores associated to self loops are set to nan
        >>> scores.iloc[0,0]=np.nan
        >>> scores.iloc[2,1]=np.nan
        >>> scores
                  gene1     gene3
        gene1       NaN  0.400157
        gene2  0.978738  2.240893
        gene3  1.867558       NaN
        >>> grn = pd.DataFrame(np.array([['gene1', 'gene2', 1],
                                         ['gene1', 'gene3', 0],
                                         ['gene3', 'gene2', 1],
                                         ['gene3', 'gene1', 0]]),
                                         columns=['TF', 'TG', 'IS_REGULATED'])
        >>> grn.index=grn['TF']+'_'+grn['TG']
        >>> grn["IS_REGULATED"] = grn["IS_REGULATED"].astype(int)
        >>> grn
                        TF     TG  IS_REGULATED
        gene1_gene2  gene1  gene2             1
        gene1_gene3  gene1  gene3             0
        gene3_gene2  gene3  gene2             1
        gene3_gene1  gene3  gene1             0
        >>> metrics = evaluate_result(scores, grn, n_links=3)
        >>> metrics
        AUROC        0.500000
        AUPR         0.791667
        Precision    1.000000
        Recall       0.500000
        Accuracy     0.666667
        F1           0.666667

    """

    y_true, y_pred, y_pred_binary = get_y_targets(scores, gold_std_grn, n_links)
    if y_true is None:
        metrics_dict = {"AUROC": 0,
                        "AUPR": 0,
                        "Precision": 0,
                        "Recall": 0,
                        "Accuracy": 0,
                        "F1": 0}
    else:
        metrics_dict = {"AUROC": roc_auc_score(y_true,y_pred),
                        "AUPR": pr_auc_score(y_true,y_pred),
                        "Precision": precision_score(y_true, y_pred_binary),
                        "Recall": recall_score(y_true, y_pred_binary),
                        "Accuracy": accuracy_score(y_true, y_pred_binary),
                        "F1": f1_score(y_true, y_pred_binary)}
    return pd.Series(metrics_dict)


def fit_beta_pdf(raw_values,xmin=0,xmax=1,nb_points=int(1e5)):
    """
    Fit a beta function to the given raw values.

    Args:
        raw_values (numpy.array): array of raw values between xmin and xmax
        xmin (int): minimum x value of beta function
        xmax (int): maximum x value of beta function
        nb_points (int): number of x points of beta function

    Returns:
        numpy.array: X values of fitted pdf
        numpy.array: y values of fitted pdf

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> values = np.random.rand(100)
        >>> X, y = fit_beta_pdf(values)

    """
    X = np.linspace(xmin, xmax, nb_points)
    ab,bb,cb,db = stats.beta.fit(raw_values)
    pdf_beta = stats.beta.pdf(X, ab, bb,cb, db)
    return X, pdf_beta


def create_random_distribution_scores(tgs, tfs):
    """
    Create random scores for the given target genes and transcription factors.
    This function is useful to evaluate the estimated GRNs (comparing to the
    GRNs of a random predictor).

    Args:
        tgs (list): list of target genes
        tfs (list): list of transcription factors

    Returns:
        pandas.DataFrame: randomly generated scores (rows = TGs ; columns = TFs)

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> tgs = ["gene1", "gene2", "gene3", "gene4", "gene5"]
        >>> tfs = ["gene1", "gene3", "gene4"]
        >>> rand_scores = create_random_distribution_scores(tgs, tfs)
        >>> rand_scores
                  gene1     gene3     gene4
        gene1       NaN  0.400157  0.978738
        gene2  2.240893  1.867558 -0.977278
        gene3  0.950088       NaN -0.103219
        gene4  0.410599  0.144044       NaN
        gene5  0.761038  0.121675  0.443863

    """
    # generating random scores for the tfs-tgs interactions
    rand = np.random.randn(len(tgs),len(tfs))
    scores_rand = pd.DataFrame(rand, index=tgs, columns=tfs)
    # deleting the self loops
    for tf in tfs:
        scores_rand[tf][tf] = None
    return scores_rand

# to be used only once - saves a file that can be used as a reference to evaluate all GRNs
def generate_rand_metrics(tgs,
                          tfs,
                          gold_std_grn,
                          n_iterations=25000,
                          path=None,
                          **eval_res_params):
    """
    Generates evaluation scores from the function evaluate_result()
    (default: AUROC, AUPR) for randomly generated GRNs.
    The random scores are given to all possible interactions tgs-tfs.
    Then this GRN is evaluated using the gold_std_grn.
    This process is repeated for n_iterations.

    Args:
        tgs (list): list of target genes
        tfs (list): list of transcription factors
        gold_std_grn (pandas.DataFrame): reference GRN used as a gold standard,
            where rows are links with names of the type <TF symbol>_<TG symbol>,
            and columns are respectively 'TF':TF symbol, 'TG':TG symbol, and
            'IS_REGULATED': indicates whether the link exists (1) or not (0)
        n_iterations (int): (default 25000) number of random GRNs to generate
        path (str): (default None) if specified, folder where to store the .csv
            file with the return matrix
        eval_res_params: (optional) parameters of called evaluate_result()
            function

    Returns:
        pandas.DataFrame: matrix
        (rows = iterations, columns = metrics of evaluated random GRN)

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> tgs = ['gene1', 'gene2', 'gene3']
        >>> tfs = ['gene1', 'gene3']
        >>> grn = pd.DataFrame(np.array([['gene1', 'gene2', 1],
                                         ['gene1', 'gene3', 0],
                                         ['gene3', 'gene2', 1],
                                         ['gene3', 'gene1', 0]]),
                                         columns=['TF', 'TG', 'IS_REGULATED'])
        >>> grn.index=grn['TF']+'_'+grn['TG']
        >>> grn["IS_REGULATED"] = grn["IS_REGULATED"].astype(int)
        >>> random_metrics = generate_rand_metrics(tgs,
                                                   tfs,
                                                   grn,
                                                   n_iterations=5)
        >>> random_metrics
           AUROC      AUPR  Precision  Recall  Accuracy        F1
        0   0.75  0.791667   1.000000     0.5      0.75  0.666667
        1   0.50  0.416667   0.666667     1.0      0.75  0.800000
        2   0.50  0.708333   1.000000     0.5      0.75  0.666667
        3   1.00  1.000000   1.000000     1.0      1.00  1.000000
        4   0.75  0.791667   1.000000     0.5      0.75  0.666667

    """

    res = []
    for i in tqdm(range(0, n_iterations)):
        scores_rand = create_random_distribution_scores(tgs, tfs)
        eval_res_params["scores"] = scores_rand
        eval_res_params["gold_std_grn"] = gold_std_grn
        metrics = evaluate_result(**eval_res_params)
        res.append(metrics)
    res = pd.DataFrame(res)
    if path:
        res.to_csv(path+".csv")
    return(res)

def compute_p_values_from_pdf(x, X, Y):
    """
    Compute the p_value of a given metric with respect to a randomized
    reference probability density function.

    Args:
        x (float): metric value to test
        X (numpy.ndarray): metric randomized reference (probability density
            function X)
        Y (numpy.ndarray): frequency randomized reference (probability density
            function Y)

    Returns:
        float: p_value of x

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> index = np.random.randint(0, 10)
        >>> X = np.random.standard_normal(10)
        >>> x = X[index]
        >>> np.random.seed(1)
        >>> Y = np.random.standard_normal(10)
        >>> p_value = compute_p_values_from_pdf(x, X, Y)
        >>> p_value
        0.008318328172202086

    """
    dx = X[1]-X[0]
    p_val = ((dx*Y)[X>=x]).sum()
    return(p_val)

def compute_p_values_from_raw_distribution(x,X_rand):
    """
    Compute the p_value of a given metric with respect to a randomized
    reference distribution (raw values).

    Args:
        x (float): metric value to test
        X_rand (numpy.ndarray): randomized reference raw values

    Returns:
        float: p_value of x

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> x = np.random.rand()
        >>> X = np.random.standard_normal(1000)
        >>> p_value = compute_p_values_from_raw_distribution(x, X)
        >>> p_value
        0.273

    """
    p_val = (X_rand >=x).sum()/X_rand.shape[0]
    return p_val


def pvalue2score(p_value):
    """
    Compute the -log10 score of a p_value.

    Args:
        p_value (float): p value

    Returns:
        float: -log10 score

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> p_value = np.random.random()
        >>> pvalue2score(p_value)
        0.2605752110604732

    """
    epsilon = 1e-300
    return(-np.log10(p_value+epsilon))


def pr_auc_score(y_true, y_pred):
    """
    Compute area under the Precision-Recall curve.

    Args:
        y_true (pandas.Series): Boolean values for the ground truth
            (correct target values)
        y_pred (pandas.Series): Continuous values from predictor

    Returns:
        float: area under the Precision-Recall curve

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> y_true = pd.Series(np.random.randint(0,2,10))
        >>> y_pred = pd.Series(np.random.randn(10))
        >>> aupr = pr_auc_score(y_true, y_pred)
        >>> aupr
        0.4755555555555555

    """
    pr_curve = precision_recall_curve(y_true,y_pred)
    aupr = auc(pr_curve[1], pr_curve[0])
    return aupr
