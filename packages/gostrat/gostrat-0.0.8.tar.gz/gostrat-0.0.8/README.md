# `gostrat`

A tool that will one day have fabulous documentation!


## Basic Usage

```
Usage:
    gostrat download_go [--obo=FN] [--gene2go=FN]
    gostrat generate_gmt [-o FN] [-t TID] [-i TYPE] [--obo=FN] [--gene2go=FN]
    gostrat (strat|stratify) [-o FN] [-f V] [-c PATT] [--invert] [--abs] [options] <gsea_fn>...
    gostrat plotconfig [-o FN] [--json] <graph_pkl>
    gostrat plot [options] [--config=FN] <graph_pkl>
```

## `download_go` - Download OBO and NCBI Gene2GO Associations

Pretty much what the heading says. All of the functions in this package use the
two files downloaded by this method. You can give your own paths for output of
the two source files. The other methods will look for these files locally
automagically, so if you specify the same paths for `--obo` and `--gene2go` on
the command line you won't have to redownload or remap anything.

## `generate_gmt` - Convert OBO and Gene2GO Associations into GMT formatted files

Generate a GMT formatted file from all GO annotations for all three namespaces
in a single GMT. `-t` allows you to generate annotations for different organisms,
e.g. 9606 for human, 10090 for mouse, etc. Probably all NCBI taxonomy IDs are
supported, but what do I know? `-i` allows you to specify which identifier type
to put into the GMT file, one of `symbol`, `entrez`, or `ensembl.gene`.

## `strat` - Do all the fancy sauce

I'll document this eventually; for now just put in a bunch of different tabular
GSEA files with GO terms as the first column and statistics/p-values as the rest
from a bunch of different experiments and the tool will probably just do its thing.
It would help if you have one column per file that ends in `padj` that contains
adjusted p-values from, say, fgsea analysis. That would be sweet.

Briefly, the algorithm casts the significant GO terms across all analyses into
a graph and groups them by taking the first neighbors of the root namespace term
(e.g. GO:0008510, Biological Process). This gives each enriched term a parent
term (which might be the term itself, depending on the significance pattern),
that allows the results to be consolidated in a possibly informative way.

To generate a fancy graphic from the results, you will need to provide the `-g`
argument with a filename, e.g. `gostrat_graph.pkl`. This will create a file named
as expected with lots of infos from the fancy sauce strat run that can be used
to generate fancy graphs with `plot`.

## `plotconfig` - Generate a plotting config file 

There are lots and lots of knobs and buttons involved with the graph viz
implemented in `plot`. These can be controlled using a config file that is
quite easily generated using this command. Simply provide the path to the
`-g` file you specified in your call to `strat` and it will spit out a
yaml formatted file to the screen for your redirection pleasure. You may
then edit this file to change parameters that you probably have no idea
what they do because I haven't documented them yet. But still, play around,
it's fun!

## `plot` - Generate graph visualizations for each GO namespace

Using the config you generated using `plotconfig` and the graph pickle from
`strat`, you should be able to create and play around with graph visualizations
of the terms in each namespace. Go ahead, try it out, it will be fun! And
probably crashy!
