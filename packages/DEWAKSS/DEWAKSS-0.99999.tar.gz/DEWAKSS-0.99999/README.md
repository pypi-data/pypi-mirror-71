<pre style="line-height: 1.2;">

                               ██╗██╗
                               ╚═╝╚═╝
    ██████╗ ███████╗██╗    ██╗ █████╗ ██╗  ██╗███████╗███████╗
    ██╔══██╗██╔════╝██║    ██║██╔══██╗██║ ██╔╝██╔════╝██╔════╝
    ██║  ██║█████╗  ██║ █╗ ██║███████║█████╔╝ ███████╗███████╗
    ██║  ██║██╔══╝  ██║███╗██║██╔══██║██╔═██╗ ╚════██║╚════██║
    ██████╔╝███████╗╚███╔███╔╝██║  ██║██║  ██╗███████║███████║
    ╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

</pre>
Denoising Expression data with a Weighted Affinity Kernel and Self-Supervision
================================================================================================

## Summary
We investigate the tuning of kNN- and diffusion-based denoising methods with a novel non-stochastic method for optimally preserving biologically relevant informative variance in single-cell data.
The framework, *Denoising Expression data with a Weighted Affinity Kernel and Self-Supervision* (DEWÄKSS), uses a self-supervised technique to tune its parameters.


<p align="center"><img src="img/fig_repo/dewakss_procedure_v2.svg" width="80%" /></p>

Install latest version by cloning this repository
```
git clone https://gitlab.com/Xparx/dewakss.git
cd dewakss
```
and then in the dewakss directory:
```
pip install .
```

For faster execution times DEWAKSS currently relies on the math kernel library ([MKL](https://software.intel.com/en-us/mkl/choose-download)) from intel. The most reliable ways to get support from MKL is to get the latest versio  of `python anaconda`. Else the latest version of MKL needs to be installed and the location to the shared object files needs to be added to `LD_LIBRARY_PATH`.


## Manuscript results
To reproduce the results from [Tjarnberg2020](https://www.biorxiv.org/content/10.1101/2020.02.28.970202v1) run the command
```
pip install DEWAKSS==0.99rc2020
```
The appropriate notebooks to follow can be found in the tag
[Tjarnberg2020](https://gitlab.com/Xparx/dewakss/-/tree/Tjarnberg2020)



## Usage

The simplest way to use DEWAKSS is to simply run the following

    import dewakss.denoise as dewakss
    
    dewaxer = dewakss.DEWAKSS(adata)
    dewaxer.fit(adata)
    dewaxer.transform(adata, copy=False)

where `adata` is either an expression matrix or an [AnnData](https://scanpy.readthedocs.io/en/stable/) object with genes as columns and cells/samples as rows.

To explore the results one can use

    dewaxer.plot_global_performance()

If one chooses to run diffusion:

    N=6
    dewaxer = dewakss.DEWAKSS(adata, iterations=N)

these can be explored using

    dewaxer.plot_diffusion_performance()
