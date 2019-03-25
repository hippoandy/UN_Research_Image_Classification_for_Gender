### gender_classification

> Requirement: ***A Server with a modern NVIDIA GPU available & tensorflow-gpu lib. for Python available***

***[IMPORTANT]*** Please prepare a machine with an ***NVIDIA GPU Device***!!!

Please refer to the TensorFlow developer site to learn how to enable GPU support for TensorFlow: [Install tensorflow-gpu](https://www.tensorflow.org/install/gpu)

For labor market project, our team also aim to provide **gendor-related analysis**. For Freelancer dataset, however, they didn't reveal the gender information for each job seeker.

We, therefore, come up with an idea to perform **image classification** using **TensorFlow-based Machine Learning model**. The program provided here, we are going to collection the profile pictures of job seekers on Freelancer based on the URLs point to the location of each profile picture that were already collected within the dataset.

***Run the Program***

1. Downloading Profile Pictures

    To download the profile images, first place our collected Freelancer dataset into the folder `gender_classification > downloading`.

    Then goto folder `gender_classification > downloading` and run the following command:
    ```bash
    $ python run.py -u 1
    ```
    This program will prompt a message and requires you to input the exact filename of the Freelancer dataset CSV file.


2. Performing Image Classification

    ***[IMPORTANT]*** Please create **2** folders under folder `gender_classification > classifing`, which are `imgs` and `training_imgs`.

    * **imgs/**: place the images you wish to do the classification on.
    * **training_imgs/**: place the training images with self-defined categories separated by folder. For example, if you have three categories of your images: `female`, `male`, and `unknown`, then the folder structure should looks like the following:
    ```txt
    +-- training_imgs/
        +-- female/
        +-- male/
        +-- unknown/
    ```
    Each folder contains the images that belong to the corresponding category.

    After the folders are created and images are placed in those folders, go inside folder `classifing`.

    ***For Windows Machine***

    Perform model retraining:
    ```bash
    $ python retrain.py --img_dir=../training_imgs
    ```
    Notes that this might take some time to finish.

    Then, perform classification on the target images:
    ```bash
    $ python label_image.py --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt \
        --input_layer=Placeholder --output_layer=final_result \
        --start 0 --concurrent 1000 --partition 1000 \
        --img_dir=../imgs/ \
        --data_file=*.jpg \
    ```

    ***For Linux-based Machine***
    Issue the following command to complete image classification:
    ```bash
    $ ./run.sh
    ```
