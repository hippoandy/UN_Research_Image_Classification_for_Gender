!#/bin/bash

python retrain.py --img_dir=../training_imgs

python label_image.py --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt \
    --input_layer=Placeholder --output_layer=final_result \
    --start 0 --concurrent 1000 --partition 1000 \
    --img_dir=../imgs/ \
    --data_file=*.jpg \