from openvino.inference_engine import IENetwork, IEPlugin
import cv2
import numpy as np
import os

def generate_feature():

    file_dir = os.listdir('../database/images')

    xml_path_fd = '../lib/face-detection-adas-0001.xml'
    bin_path_fd = '../lib/face-detection-adas-0001.bin'

    xml_path_fr = '../lib/face-reidentification-retail-0095.xml'
    bin_path_fr = '../lib/face-reidentification-retail-0095.bin'

    cpu_extension_path = 'cpu_extension_avx2.dll'

    net_fd = IENetwork(model = xml_path_fd, weights = bin_path_fd)
    net_fr = IENetwork(model = xml_path_fr, weights = bin_path_fr)

    input_blob_fd = next(iter(net_fd.inputs))
    out_blob_fd = next(iter(net_fd.outputs))

    input_blob_fr = next(iter(net_fr.inputs))
    out_blob_fr = next(iter(net_fr.outputs))

    device = 'CPU'

    plugin = IEPlugin(device = device, plugin_dirs = None)
    plugin.add_cpu_extension(cpu_extension_path)

    exec_net_fd = plugin.load(network = net_fd, num_requests=2)
    exec_net_fr = plugin.load(network = net_fr, num_requests=2)

    n_fd, c_fd, h_fd, w_fd = net_fd.inputs[input_blob_fd].shape
    n_fr, c_fr, h_fr, w_fr = net_fr.inputs[input_blob_fr].shape

    for i in file_dir:

        registration_image = cv2.imread('../database/images/' + i)

        initial_h, initial_w = registration_image.shape[:-1]

        registration_image_resize = cv2.resize(registration_image, (w_fd, h_fd))
        registration_image_resize = registration_image_resize.transpose((2, 0, 1))  # Change data layout from HWC to CHW

        res_fd = exec_net_fd.infer(inputs = {input_blob_fd: registration_image_resize})
        res_fd = res_fd[out_blob_fd]

        x_min = int(res_fd[0][0][0][3] * initial_w)
        y_min = int(res_fd[0][0][0][4] * initial_h)
        x_max = int(res_fd[0][0][0][5] * initial_w)
        y_max = int(res_fd[0][0][0][6] * initial_h)

        confidence = int(res_fd[0][0][0][2] * 100) / 100  # keep two decimal

        if confidence > 0.7:
            cv2.rectangle(registration_image, (x_min, y_min), (x_max, y_max), (232, 35, 244), 1, 1)
            cv2.putText(registration_image, "Conf:" + str(confidence), (x_min + 5, y_min + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            face_image = registration_image[y_min:y_max, x_min:x_max]

            face_image_fr = cv2.resize(face_image, (w_fr, h_fr))
            face_image_fr = face_image_fr.transpose((2, 0, 1))

            res_fr = exec_net_fr.infer(inputs={input_blob_fr: face_image_fr})

            registration_image_vector = res_fr[out_blob_fr]
            face_feature_vector = registration_image_vector[0][:].reshape(-1)
            cv2.imwrite(i, registration_image)


            np.savetxt('../database/features/' + i.split('.')[0] + '.txt', face_feature_vector)

        else:
            print("Don't find face in the image of " + i)
            continue


generate_feature()