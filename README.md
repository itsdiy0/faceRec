# faceRec
![example](https://i.ibb.co/jZwJMbS/Screenshot-from-2024-01-18-12-41-42.png)
![example](https://i.ibb.co/0VL1GgX/test2-ss.png)
<br>

installing requirements : 
```bash
pip install flask
pip install numpy
pip install opencv_contrib_python
```
face recognition system using OpenCV and Flask<br>this project is based on training pictures of different people faces, and then comparing any face with trained faces;<br>
in result it will show the similarity percentage between the picture and trained model<br>

notes : <ul>
<li> before running recegniton action, please add enough faces to the database for an accurate training result </li>
<li> number of faces from each person for training purpose must be equal, otherwise it will lead to wrong answers </li>
<li> you can remove persons from database in "View users" section, remember the equality number of pictures between train elements </li>
<li> run the project by running app.py </li>
</ul>

