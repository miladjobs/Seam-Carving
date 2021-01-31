# Seam Carving
This project is my Algorithm project for detect Seams in images and delete them for resize image.You can see project sources in this [link](https://github.com/miladjobs/Seam-Carving)

# Introduction
In this project first we calculate energy of image and then we find seam via dijkstra algorithm to fine minimum path between pixel with mimum energy

# Time and Space Complexity
* Time Complexity:There is one subproblem corresponding to each pixel in the original image. For each subproblems, there are at most 3 dependencies, so we do a constant amount of work to solve each subproblem. Finally, we go through the last row one more time. Thus, if the image is W pixels wide and H pixels tall, the time complexity is O(W×H+W).
* Space Complexity: At each time, we store two lists, one for the previous row and one for the current row. The first one has W elements, and second one grows to have W elements at most. Thus, the space complexity is O(2W), which is simply O(W).

# Installation
Install the dependencies
```sh
(venv)$ pip install -r requirements.txt
```
# Run
```sh
(venv)$ python main.py -i ../samples/input/2.png -x 100 -y 100 -o ../samples/output/
```
where
* -i : input image file path
* -x : number of vertical pixels to reduce
* -y : number of horizontal pixles to reduce
* -o : ouput directory(default: input directory)

# Sample
* input image:
<div align="center">

![inputimage](https://github.com/miladjobs/Seam-Carving/blob/main/samples/input/2.png?raw=true)

</div>

* output image:
<div align="center">

![inputimage](https://github.com/miladjobs/Seam-Carving/blob/main/samples/output/2_out.png?raw=true)

</div>
* process gif:
<div align="center">

![inputimage](https://github.com/miladjobs/Seam-Carving/blob/main/samples/output/2_out.gif?raw=true)

</div>

Watch gif in tis [link](https://github.com/miladjobs/Seam-Carving/blob/main/samples/output/2_out.gif)
