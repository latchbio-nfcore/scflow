from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], qc_min_ribo: typing.Optional[float], mult_doublet_rate: typing.Optional[float], integ_small_clust_thresh: typing.Optional[int], manifest: str, input: str, ensembl_mappings: str, ctd_path: str, celltype_mappings: typing.Optional[str], reddim_genes_yml: typing.Optional[str], species: str, qc_key_colname: str, qc_factor_vars: str, qc_min_library_size: int, qc_max_library_size: str, qc_min_features: int, qc_max_features: str, qc_max_ribo: float, qc_max_mito: str, qc_min_counts: int, qc_min_cells: int, qc_drop_unmapped: str, qc_drop_mito: str, qc_drop_ribo: str, qc_nmads: float, amb_find_cells: str, amb_retain: str, amb_lower: int, amb_alpha_cutoff: float, amb_niters: int, amb_expect_cells: int, mult_find_singlets: str, mult_singlets_method: str, mult_vars_to_regress_out: str, mult_pca_dims: int, mult_var_features: int, mult_dpk: int, mult_pK: float, merge_plot_vars: str, merge_facet_vars: str, merge_outlier_vars: str, integ_method: str, integ_unique_id_var: str, integ_take_gene_union: str, integ_remove_missing: str, integ_num_genes: int, integ_combine: str, integ_keep_unique: str, integ_capitalize: str, integ_use_cols: str, integ_k: int, integ_lambda: float, integ_thresh: float, integ_max_iters: int, integ_nrep: int, integ_rand_seed: int, integ_knn_k: int, integ_k2: int, integ_prune_thresh: float, integ_ref_dataset: str, integ_min_cells: int, integ_quantiles: int, integ_nstart: int, integ_resolution: int, integ_dims_use: str, integ_dist_use: str, integ_center: str, integ_categorical_covariates: str, integ_input_reduced_dim: str, reddim_input_reduced_dim: str, reddim_reduction_methods: str, reddim_vars_to_regress_out: str, reddim_umap_pca_dims: int, reddim_umap_n_neighbors: int, reddim_umap_n_components: int, reddim_umap_init: str, reddim_umap_metric: str, reddim_umap_n_epochs: int, reddim_umap_learning_rate: int, reddim_umap_min_dist: float, reddim_umap_spread: float, reddim_umap_set_op_mix_ratio: float, reddim_umap_local_connectivity: int, reddim_umap_repulsion_strength: int, reddim_umap_negative_sample_rate: int, reddim_umap_fast_sgd: str, reddim_tsne_dims: int, reddim_tsne_initial_dims: int, reddim_tsne_perplexity: int, reddim_tsne_theta: float, reddim_tsne_stop_lying_iter: int, reddim_tsne_mom_switch_iter: int, reddim_tsne_max_iter: int, reddim_tsne_pca_center: str, reddim_tsne_pca_scale: str, reddim_tsne_normalize: str, reddim_tsne_momentum: float, reddim_tsne_final_momentum: float, reddim_tsne_eta: int, reddim_tsne_exaggeration_factor: int, clust_cluster_method: str, clust_reduction_method: str, clust_res: float, clust_k: int, clust_louvain_iter: int, cta_clusters_colname: str, cta_cells_to_sample: int, cta_unique_id_var: str, cta_celltype_var: str, cta_facet_vars: str, cta_metric_vars: str, cta_top_n: int, dge_de_method: str, dge_mast_method: str, dge_min_counts: int, dge_min_cells_pc: float, dge_rescale_numerics: str, dge_pseudobulk: str, dge_celltype_var: str, dge_sample_var: str, dge_dependent_var: str, dge_ref_class: str, dge_confounding_vars: str, dge_random_effects_var: str, dge_fc_threshold: float, dge_pval_cutoff: float, dge_force_run: str, dge_max_cores: str, ipa_enrichment_tool: str, ipa_enrichment_method: str, ipa_enrichment_database: str, dirich_unique_id_var: str, dirich_celltype_var: str, dirich_dependent_var: str, dirich_ref_class: str, dirich_var_order: str, plotreddim_reduction_methods: str, reddimplot_pointsize: float, reddimplot_alpha: float) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('manifest', manifest),
                *get_flag('input', input),
                *get_flag('ensembl_mappings', ensembl_mappings),
                *get_flag('ctd_path', ctd_path),
                *get_flag('celltype_mappings', celltype_mappings),
                *get_flag('reddim_genes_yml', reddim_genes_yml),
                *get_flag('species', species),
                *get_flag('outdir', outdir),
                *get_flag('qc_key_colname', qc_key_colname),
                *get_flag('qc_factor_vars', qc_factor_vars),
                *get_flag('qc_min_library_size', qc_min_library_size),
                *get_flag('qc_max_library_size', qc_max_library_size),
                *get_flag('qc_min_features', qc_min_features),
                *get_flag('qc_max_features', qc_max_features),
                *get_flag('qc_min_ribo', qc_min_ribo),
                *get_flag('qc_max_ribo', qc_max_ribo),
                *get_flag('qc_max_mito', qc_max_mito),
                *get_flag('qc_min_counts', qc_min_counts),
                *get_flag('qc_min_cells', qc_min_cells),
                *get_flag('qc_drop_unmapped', qc_drop_unmapped),
                *get_flag('qc_drop_mito', qc_drop_mito),
                *get_flag('qc_drop_ribo', qc_drop_ribo),
                *get_flag('qc_nmads', qc_nmads),
                *get_flag('amb_find_cells', amb_find_cells),
                *get_flag('amb_retain', amb_retain),
                *get_flag('amb_lower', amb_lower),
                *get_flag('amb_alpha_cutoff', amb_alpha_cutoff),
                *get_flag('amb_niters', amb_niters),
                *get_flag('amb_expect_cells', amb_expect_cells),
                *get_flag('mult_find_singlets', mult_find_singlets),
                *get_flag('mult_singlets_method', mult_singlets_method),
                *get_flag('mult_vars_to_regress_out', mult_vars_to_regress_out),
                *get_flag('mult_pca_dims', mult_pca_dims),
                *get_flag('mult_var_features', mult_var_features),
                *get_flag('mult_doublet_rate', mult_doublet_rate),
                *get_flag('mult_dpk', mult_dpk),
                *get_flag('mult_pK', mult_pK),
                *get_flag('merge_plot_vars', merge_plot_vars),
                *get_flag('merge_facet_vars', merge_facet_vars),
                *get_flag('merge_outlier_vars', merge_outlier_vars),
                *get_flag('integ_method', integ_method),
                *get_flag('integ_unique_id_var', integ_unique_id_var),
                *get_flag('integ_take_gene_union', integ_take_gene_union),
                *get_flag('integ_remove_missing', integ_remove_missing),
                *get_flag('integ_num_genes', integ_num_genes),
                *get_flag('integ_combine', integ_combine),
                *get_flag('integ_keep_unique', integ_keep_unique),
                *get_flag('integ_capitalize', integ_capitalize),
                *get_flag('integ_use_cols', integ_use_cols),
                *get_flag('integ_k', integ_k),
                *get_flag('integ_lambda', integ_lambda),
                *get_flag('integ_thresh', integ_thresh),
                *get_flag('integ_max_iters', integ_max_iters),
                *get_flag('integ_nrep', integ_nrep),
                *get_flag('integ_rand_seed', integ_rand_seed),
                *get_flag('integ_knn_k', integ_knn_k),
                *get_flag('integ_k2', integ_k2),
                *get_flag('integ_prune_thresh', integ_prune_thresh),
                *get_flag('integ_ref_dataset', integ_ref_dataset),
                *get_flag('integ_min_cells', integ_min_cells),
                *get_flag('integ_quantiles', integ_quantiles),
                *get_flag('integ_nstart', integ_nstart),
                *get_flag('integ_resolution', integ_resolution),
                *get_flag('integ_dims_use', integ_dims_use),
                *get_flag('integ_dist_use', integ_dist_use),
                *get_flag('integ_center', integ_center),
                *get_flag('integ_small_clust_thresh', integ_small_clust_thresh),
                *get_flag('integ_categorical_covariates', integ_categorical_covariates),
                *get_flag('integ_input_reduced_dim', integ_input_reduced_dim),
                *get_flag('reddim_input_reduced_dim', reddim_input_reduced_dim),
                *get_flag('reddim_reduction_methods', reddim_reduction_methods),
                *get_flag('reddim_vars_to_regress_out', reddim_vars_to_regress_out),
                *get_flag('reddim_umap_pca_dims', reddim_umap_pca_dims),
                *get_flag('reddim_umap_n_neighbors', reddim_umap_n_neighbors),
                *get_flag('reddim_umap_n_components', reddim_umap_n_components),
                *get_flag('reddim_umap_init', reddim_umap_init),
                *get_flag('reddim_umap_metric', reddim_umap_metric),
                *get_flag('reddim_umap_n_epochs', reddim_umap_n_epochs),
                *get_flag('reddim_umap_learning_rate', reddim_umap_learning_rate),
                *get_flag('reddim_umap_min_dist', reddim_umap_min_dist),
                *get_flag('reddim_umap_spread', reddim_umap_spread),
                *get_flag('reddim_umap_set_op_mix_ratio', reddim_umap_set_op_mix_ratio),
                *get_flag('reddim_umap_local_connectivity', reddim_umap_local_connectivity),
                *get_flag('reddim_umap_repulsion_strength', reddim_umap_repulsion_strength),
                *get_flag('reddim_umap_negative_sample_rate', reddim_umap_negative_sample_rate),
                *get_flag('reddim_umap_fast_sgd', reddim_umap_fast_sgd),
                *get_flag('reddim_tsne_dims', reddim_tsne_dims),
                *get_flag('reddim_tsne_initial_dims', reddim_tsne_initial_dims),
                *get_flag('reddim_tsne_perplexity', reddim_tsne_perplexity),
                *get_flag('reddim_tsne_theta', reddim_tsne_theta),
                *get_flag('reddim_tsne_stop_lying_iter', reddim_tsne_stop_lying_iter),
                *get_flag('reddim_tsne_mom_switch_iter', reddim_tsne_mom_switch_iter),
                *get_flag('reddim_tsne_max_iter', reddim_tsne_max_iter),
                *get_flag('reddim_tsne_pca_center', reddim_tsne_pca_center),
                *get_flag('reddim_tsne_pca_scale', reddim_tsne_pca_scale),
                *get_flag('reddim_tsne_normalize', reddim_tsne_normalize),
                *get_flag('reddim_tsne_momentum', reddim_tsne_momentum),
                *get_flag('reddim_tsne_final_momentum', reddim_tsne_final_momentum),
                *get_flag('reddim_tsne_eta', reddim_tsne_eta),
                *get_flag('reddim_tsne_exaggeration_factor', reddim_tsne_exaggeration_factor),
                *get_flag('clust_cluster_method', clust_cluster_method),
                *get_flag('clust_reduction_method', clust_reduction_method),
                *get_flag('clust_res', clust_res),
                *get_flag('clust_k', clust_k),
                *get_flag('clust_louvain_iter', clust_louvain_iter),
                *get_flag('cta_clusters_colname', cta_clusters_colname),
                *get_flag('cta_cells_to_sample', cta_cells_to_sample),
                *get_flag('cta_unique_id_var', cta_unique_id_var),
                *get_flag('cta_celltype_var', cta_celltype_var),
                *get_flag('cta_facet_vars', cta_facet_vars),
                *get_flag('cta_metric_vars', cta_metric_vars),
                *get_flag('cta_top_n', cta_top_n),
                *get_flag('dge_de_method', dge_de_method),
                *get_flag('dge_mast_method', dge_mast_method),
                *get_flag('dge_min_counts', dge_min_counts),
                *get_flag('dge_min_cells_pc', dge_min_cells_pc),
                *get_flag('dge_rescale_numerics', dge_rescale_numerics),
                *get_flag('dge_pseudobulk', dge_pseudobulk),
                *get_flag('dge_celltype_var', dge_celltype_var),
                *get_flag('dge_sample_var', dge_sample_var),
                *get_flag('dge_dependent_var', dge_dependent_var),
                *get_flag('dge_ref_class', dge_ref_class),
                *get_flag('dge_confounding_vars', dge_confounding_vars),
                *get_flag('dge_random_effects_var', dge_random_effects_var),
                *get_flag('dge_fc_threshold', dge_fc_threshold),
                *get_flag('dge_pval_cutoff', dge_pval_cutoff),
                *get_flag('dge_force_run', dge_force_run),
                *get_flag('dge_max_cores', dge_max_cores),
                *get_flag('ipa_enrichment_tool', ipa_enrichment_tool),
                *get_flag('ipa_enrichment_method', ipa_enrichment_method),
                *get_flag('ipa_enrichment_database', ipa_enrichment_database),
                *get_flag('dirich_unique_id_var', dirich_unique_id_var),
                *get_flag('dirich_celltype_var', dirich_celltype_var),
                *get_flag('dirich_dependent_var', dirich_dependent_var),
                *get_flag('dirich_ref_class', dirich_ref_class),
                *get_flag('dirich_var_order', dirich_var_order),
                *get_flag('plotreddim_reduction_methods', plotreddim_reduction_methods),
                *get_flag('reddimplot_pointsize', reddimplot_pointsize),
                *get_flag('reddimplot_alpha', reddimplot_alpha)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_scflow", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_scflow(outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], qc_min_ribo: typing.Optional[float], mult_doublet_rate: typing.Optional[float], integ_small_clust_thresh: typing.Optional[int], manifest: str = './refs/Manifest.txt', input: str = './refs/SampleSheet.tsv', ensembl_mappings: str = 'https://raw.githubusercontent.com/nf-core/test-datasets/scflow/assets/ensembl_mappings.tsv', ctd_path: str = 'https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/28033407/ctd_v1.zip', celltype_mappings: typing.Optional[str] = './conf/celltype_mappings.tsv', reddim_genes_yml: typing.Optional[str] = './conf/reddim_genes.yml', species: str = 'human', qc_key_colname: str = 'manifest', qc_factor_vars: str = 'seqdate', qc_min_library_size: int = 250, qc_max_library_size: str = 'adaptive', qc_min_features: int = 100, qc_max_features: str = 'adaptive', qc_max_ribo: float = 1, qc_max_mito: str = 'adaptive', qc_min_counts: int = 2, qc_min_cells: int = 2, qc_drop_unmapped: str = 'True', qc_drop_mito: str = 'True', qc_drop_ribo: str = 'false', qc_nmads: float = 4, amb_find_cells: str = 'true', amb_retain: str = 'auto', amb_lower: int = 100, amb_alpha_cutoff: float = 0.001, amb_niters: int = 10000, amb_expect_cells: int = 3000, mult_find_singlets: str = 'true', mult_singlets_method: str = 'doubletfinder', mult_vars_to_regress_out: str = 'nCount_RNA,pc_mito', mult_pca_dims: int = 10, mult_var_features: int = 2000, mult_dpk: int = 8, mult_pK: float = 0.02, merge_plot_vars: str = 'total_features_by_counts,total_counts,pc_mito,pc_ribo', merge_facet_vars: str = 'NULL', merge_outlier_vars: str = 'total_features_by_counts,total_counts', integ_method: str = 'Liger', integ_unique_id_var: str = 'manifest', integ_take_gene_union: str = 'false', integ_remove_missing: str = 'true', integ_num_genes: int = 3000, integ_combine: str = 'union', integ_keep_unique: str = 'false', integ_capitalize: str = 'false', integ_use_cols: str = 'true', integ_k: int = 30, integ_lambda: float = 5, integ_thresh: float = 0.0001, integ_max_iters: int = 100, integ_nrep: int = 1, integ_rand_seed: int = 1, integ_knn_k: int = 20, integ_k2: int = 500, integ_prune_thresh: float = 0.2, integ_ref_dataset: str = 'NULL', integ_min_cells: int = 2, integ_quantiles: int = 50, integ_nstart: int = 10, integ_resolution: int = 1, integ_dims_use: str = 'NULL', integ_dist_use: str = 'CR', integ_center: str = 'false', integ_categorical_covariates: str = 'individual,diagnosis,region,sex', integ_input_reduced_dim: str = 'UMAP', reddim_input_reduced_dim: str = 'PCA,Liger', reddim_reduction_methods: str = 'tSNE,UMAP,UMAP3D', reddim_vars_to_regress_out: str = 'nCount_RNA,pc_mito', reddim_umap_pca_dims: int = 30, reddim_umap_n_neighbors: int = 35, reddim_umap_n_components: int = 2, reddim_umap_init: str = 'spectral', reddim_umap_metric: str = 'euclidean', reddim_umap_n_epochs: int = 200, reddim_umap_learning_rate: int = 1, reddim_umap_min_dist: float = 0.4, reddim_umap_spread: float = 0.85, reddim_umap_set_op_mix_ratio: float = 1, reddim_umap_local_connectivity: int = 1, reddim_umap_repulsion_strength: int = 1, reddim_umap_negative_sample_rate: int = 5, reddim_umap_fast_sgd: str = 'false', reddim_tsne_dims: int = 2, reddim_tsne_initial_dims: int = 50, reddim_tsne_perplexity: int = 150, reddim_tsne_theta: float = 0.5, reddim_tsne_stop_lying_iter: int = 250, reddim_tsne_mom_switch_iter: int = 250, reddim_tsne_max_iter: int = 1000, reddim_tsne_pca_center: str = 'true', reddim_tsne_pca_scale: str = 'false', reddim_tsne_normalize: str = 'true', reddim_tsne_momentum: float = 0.5, reddim_tsne_final_momentum: float = 0.8, reddim_tsne_eta: int = 1000, reddim_tsne_exaggeration_factor: int = 12, clust_cluster_method: str = 'leiden', clust_reduction_method: str = 'UMAP_Liger', clust_res: float = 0.001, clust_k: int = 50, clust_louvain_iter: int = 1, cta_clusters_colname: str = 'clusters', cta_cells_to_sample: int = 10000, cta_unique_id_var: str = 'individual', cta_celltype_var: str = 'cluster_celltype', cta_facet_vars: str = 'manifest,diagnosis,sex,capdate,prepdate,seqdate', cta_metric_vars: str = 'pc_mito,pc_ribo,total_counts,total_features_by_counts', cta_top_n: int = 5, dge_de_method: str = 'MASTZLM', dge_mast_method: str = 'bayesglm', dge_min_counts: int = 1, dge_min_cells_pc: float = 0.1, dge_rescale_numerics: str = 'true', dge_pseudobulk: str = 'false', dge_celltype_var: str = 'cluster_celltype', dge_sample_var: str = 'manifest', dge_dependent_var: str = 'group', dge_ref_class: str = 'Control', dge_confounding_vars: str = 'cngeneson,seqdate,pc_mito', dge_random_effects_var: str = 'NULL', dge_fc_threshold: float = 1.1, dge_pval_cutoff: float = 0.05, dge_force_run: str = 'false', dge_max_cores: str = "'null'", ipa_enrichment_tool: str = 'WebGestaltR', ipa_enrichment_method: str = 'ORA', ipa_enrichment_database: str = 'GO_Biological_Process', dirich_unique_id_var: str = 'individual', dirich_celltype_var: str = 'cluster_celltype', dirich_dependent_var: str = 'group', dirich_ref_class: str = 'Control', dirich_var_order: str = 'Control,Low,High', plotreddim_reduction_methods: str = 'UMAP_Liger', reddimplot_pointsize: float = 0.1, reddimplot_alpha: float = 0.2) -> None:
    """
    nf-core/scflow

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, manifest=manifest, input=input, ensembl_mappings=ensembl_mappings, ctd_path=ctd_path, celltype_mappings=celltype_mappings, reddim_genes_yml=reddim_genes_yml, species=species, outdir=outdir, qc_key_colname=qc_key_colname, qc_factor_vars=qc_factor_vars, qc_min_library_size=qc_min_library_size, qc_max_library_size=qc_max_library_size, qc_min_features=qc_min_features, qc_max_features=qc_max_features, qc_min_ribo=qc_min_ribo, qc_max_ribo=qc_max_ribo, qc_max_mito=qc_max_mito, qc_min_counts=qc_min_counts, qc_min_cells=qc_min_cells, qc_drop_unmapped=qc_drop_unmapped, qc_drop_mito=qc_drop_mito, qc_drop_ribo=qc_drop_ribo, qc_nmads=qc_nmads, amb_find_cells=amb_find_cells, amb_retain=amb_retain, amb_lower=amb_lower, amb_alpha_cutoff=amb_alpha_cutoff, amb_niters=amb_niters, amb_expect_cells=amb_expect_cells, mult_find_singlets=mult_find_singlets, mult_singlets_method=mult_singlets_method, mult_vars_to_regress_out=mult_vars_to_regress_out, mult_pca_dims=mult_pca_dims, mult_var_features=mult_var_features, mult_doublet_rate=mult_doublet_rate, mult_dpk=mult_dpk, mult_pK=mult_pK, merge_plot_vars=merge_plot_vars, merge_facet_vars=merge_facet_vars, merge_outlier_vars=merge_outlier_vars, integ_method=integ_method, integ_unique_id_var=integ_unique_id_var, integ_take_gene_union=integ_take_gene_union, integ_remove_missing=integ_remove_missing, integ_num_genes=integ_num_genes, integ_combine=integ_combine, integ_keep_unique=integ_keep_unique, integ_capitalize=integ_capitalize, integ_use_cols=integ_use_cols, integ_k=integ_k, integ_lambda=integ_lambda, integ_thresh=integ_thresh, integ_max_iters=integ_max_iters, integ_nrep=integ_nrep, integ_rand_seed=integ_rand_seed, integ_knn_k=integ_knn_k, integ_k2=integ_k2, integ_prune_thresh=integ_prune_thresh, integ_ref_dataset=integ_ref_dataset, integ_min_cells=integ_min_cells, integ_quantiles=integ_quantiles, integ_nstart=integ_nstart, integ_resolution=integ_resolution, integ_dims_use=integ_dims_use, integ_dist_use=integ_dist_use, integ_center=integ_center, integ_small_clust_thresh=integ_small_clust_thresh, integ_categorical_covariates=integ_categorical_covariates, integ_input_reduced_dim=integ_input_reduced_dim, reddim_input_reduced_dim=reddim_input_reduced_dim, reddim_reduction_methods=reddim_reduction_methods, reddim_vars_to_regress_out=reddim_vars_to_regress_out, reddim_umap_pca_dims=reddim_umap_pca_dims, reddim_umap_n_neighbors=reddim_umap_n_neighbors, reddim_umap_n_components=reddim_umap_n_components, reddim_umap_init=reddim_umap_init, reddim_umap_metric=reddim_umap_metric, reddim_umap_n_epochs=reddim_umap_n_epochs, reddim_umap_learning_rate=reddim_umap_learning_rate, reddim_umap_min_dist=reddim_umap_min_dist, reddim_umap_spread=reddim_umap_spread, reddim_umap_set_op_mix_ratio=reddim_umap_set_op_mix_ratio, reddim_umap_local_connectivity=reddim_umap_local_connectivity, reddim_umap_repulsion_strength=reddim_umap_repulsion_strength, reddim_umap_negative_sample_rate=reddim_umap_negative_sample_rate, reddim_umap_fast_sgd=reddim_umap_fast_sgd, reddim_tsne_dims=reddim_tsne_dims, reddim_tsne_initial_dims=reddim_tsne_initial_dims, reddim_tsne_perplexity=reddim_tsne_perplexity, reddim_tsne_theta=reddim_tsne_theta, reddim_tsne_stop_lying_iter=reddim_tsne_stop_lying_iter, reddim_tsne_mom_switch_iter=reddim_tsne_mom_switch_iter, reddim_tsne_max_iter=reddim_tsne_max_iter, reddim_tsne_pca_center=reddim_tsne_pca_center, reddim_tsne_pca_scale=reddim_tsne_pca_scale, reddim_tsne_normalize=reddim_tsne_normalize, reddim_tsne_momentum=reddim_tsne_momentum, reddim_tsne_final_momentum=reddim_tsne_final_momentum, reddim_tsne_eta=reddim_tsne_eta, reddim_tsne_exaggeration_factor=reddim_tsne_exaggeration_factor, clust_cluster_method=clust_cluster_method, clust_reduction_method=clust_reduction_method, clust_res=clust_res, clust_k=clust_k, clust_louvain_iter=clust_louvain_iter, cta_clusters_colname=cta_clusters_colname, cta_cells_to_sample=cta_cells_to_sample, cta_unique_id_var=cta_unique_id_var, cta_celltype_var=cta_celltype_var, cta_facet_vars=cta_facet_vars, cta_metric_vars=cta_metric_vars, cta_top_n=cta_top_n, dge_de_method=dge_de_method, dge_mast_method=dge_mast_method, dge_min_counts=dge_min_counts, dge_min_cells_pc=dge_min_cells_pc, dge_rescale_numerics=dge_rescale_numerics, dge_pseudobulk=dge_pseudobulk, dge_celltype_var=dge_celltype_var, dge_sample_var=dge_sample_var, dge_dependent_var=dge_dependent_var, dge_ref_class=dge_ref_class, dge_confounding_vars=dge_confounding_vars, dge_random_effects_var=dge_random_effects_var, dge_fc_threshold=dge_fc_threshold, dge_pval_cutoff=dge_pval_cutoff, dge_force_run=dge_force_run, dge_max_cores=dge_max_cores, ipa_enrichment_tool=ipa_enrichment_tool, ipa_enrichment_method=ipa_enrichment_method, ipa_enrichment_database=ipa_enrichment_database, dirich_unique_id_var=dirich_unique_id_var, dirich_celltype_var=dirich_celltype_var, dirich_dependent_var=dirich_dependent_var, dirich_ref_class=dirich_ref_class, dirich_var_order=dirich_var_order, plotreddim_reduction_methods=plotreddim_reduction_methods, reddimplot_pointsize=reddimplot_pointsize, reddimplot_alpha=reddimplot_alpha)

