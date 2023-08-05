---
title: Manual
parent: home
---

## Execute the Jupyter notebooks

This course content is provided as Jupyter notebooks that require to be powered by a Jupyter server with Python3 kernel.

## Install Jupyter

### First install Anaconda

[Anaconda](https://www.anaconda.com/distribution) is complete and easy to install.
In particular, it is shipped with:

- [Jupyter](http://jupyter.org/)
- The [Spyder](https://github.com/spyder-ide/spyder) IDE
- Scipy libraries: Numpy, Pandas, etc.

For a detailed installation of Anaconda and its extensions on Windows, Mac or Linux, follow the <a href="pages/anaconda.md"><img src="fig/anaconda.png" style="display:inline" alt="Anaconda logo" width="100px"></a> instructions.

### Finalize installation with conda

From the project root directory, type:

```bash
conda install --file requirements.txt
```

## Run a Jupyter server

- Either from Anaconda graphical interface
- or the command line interface from the project root directory:

```bash
jupyter-notebook
```

## Convert to html, slideshow and pdf

Use [nbcourse](https://gitlab.math.unistra.fr/boileau/nbcourse):

```bash
nbcourse list
build_book          Build pdf book
build_pages         Build html pages
convert_to_html     Convert executed notebook to html page
convert_to_slides   Convert executed notebook to reveal slides
copy_material       Copy notebook and theme material to output directory
copy_reveal         Copy reveal.js to output directory
execute_notebooks   Write executed notebooks to output directory
output_dir          Create empty output directory
zip_archive         Build a single zip archive for all material
zip_chapters        Build zip archives for single chapter downloads
```

Edit the `nbcourse.yml` file and run:

```bash
nbcourse [-n 4] <target>  # [to run on 4 parallel threads]
```

The result will be located in `build/` directory.

## Publish with GitLab Pages

Thanks to [.gitlab-ci.yml](.gitlab-ci.yml) file, an online version may be automatically published at every `git push` towards a GitLab project.
