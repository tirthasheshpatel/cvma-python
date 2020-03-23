echo "starting..."

python3 -m numpydoc cvma.utils > ./docs/cvma/utils.rst
python3 -m numpydoc cvma.utils.to_homogeneous >> ./docs/cvma/utils.rst
python3 -m numpydoc cvma.chapter_one > ./docs/cvma/chapter_one.rst
python3 -m numpydoc cvma.chapter_one.get_rotation_matrix >> ./docs/cvma/chapter_one.rst
python3 -m numpydoc cvma.chapter_one.Camera >> ./docs/cvma/chapter_one.rst

