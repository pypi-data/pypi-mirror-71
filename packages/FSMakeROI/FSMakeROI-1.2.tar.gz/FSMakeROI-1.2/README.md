# FSMakeROI
A CLI tool to convert Freesurfer segmentations into separate NifTi
files

## Installation
Install this package using `pip` with:

```
pip install fsmakeroi
```

## Usage
The command context for running this tool is:

```
fsmakeroi [OPTIONS] aseg rois
```

Where `aseg` is the path to aparc+aseg.mgz file, and `rois` is the
the path to text file containing Freesurfer ROI LUT codes.

The ROI code file is a list of ROIs to extract, with each line being
the code to corresponding ROI. Please refer to 
/examples/example_rois.txt for an example on creating the code file.

ROIs can also be applied to any images as long as they are registered
to T1 in Freesurfer space. This is done with the `-i` or `--image`
flag:

```
fsmakeroi -i [PATH TO IMAGE] aseg rois
```
