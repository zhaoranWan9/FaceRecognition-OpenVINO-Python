from openvino.inference_engine import IENetwork, IEPlugin
import cv2
import time
import numpy as np
import os
import database.database

def face_recognition():
    feature_dir = os.listdir('../database/features')
    image_dir = os.listdir('../database/images')


    xml_path_fd = '../lib/face-detection-adas-0001.xml'
    bin_path_fd = '../lib/face-detection-adas-0001.bin'

    xml_path_fr = '../lib/face-reidentification-retail-0095.xml'
    bin_path_fr = '../lib/face-reidentification-retail-0095.bin'

    xml_path_fa = '../lib/age-gender-recognition-retail-0013.xml'
    bin_path_fa = '../lib/age-gender-recognition-retail-0013.bin'


    cpu_extension_path = 'cpu_extension_avx2.dll'

    net_fd = IENetwork(model = xml_path_fd, weights = bin_path_fd)
    net_fr = IENetwork(model = xml_path_fr, weights = bin_path_fr)
    net_fa = IENetwork(model = xml_path_fa, weights = bin_path_fa)

    input_blob_fd = next(iter(net_fd.inputs))
    out_blob_fd = next(iter(net_fd.outputs))

    input_blob_fr = next(iter(net_fr.inputs))
    out_blob_fr = next(iter(net_fr.outputs))

    input_blob_fa = next(iter(net_fa.inputs))
    out_blob_fa = next(iter(net_fa.outputs))

    device = 'CPU'

    plugin = IEPlugin(device = device, plugin_dirs = None)
    plugin.add_cpu_extension(cpu_extension_path)

    exec_net = plugin.load(network = net_fd, num_requests = 2)
    exec_net2 = plugin.load(network = net_fr, num_requests = 2)
    exec_net3 = plugin.load(network = net_fa, num_requests = 2)

    n_fd, c_fd, h_fd, w_fd = net_fd.inputs[input_blob_fd].shape
    n_fr, c_fr, h_fr, w_fr = net_fr.inputs[input_blob_fr].shape
    n_fa, c_fa, h_fa, w_fa = net_fa.inputs[input_blob_fa].shape


    database_feature_list = database.database.load()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    start_time = time.time()
    counter = 0

    index = 0

    while (cap.isOpened()):

        ret, frame = cap.read()
        initial_h, initial_w = frame.shape[:-1]
        frame_resize = cv2.resize(frame, (w_fd, h_fd))
        frame_resize = frame_resize.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        frame_resize = frame_resize.reshape((n_fd, c_fd, h_fd, w_fd))

        res_fd = exec_net.infer(inputs={input_blob_fd: frame_resize})
        res_fd = res_fd[out_blob_fd]


        counter += 1
        if (time.time() - start_time) != 0:
            cv2.putText(frame, "FPS {0}".format(float('%.1f' % (counter / (time.time() - start_time)))), (500, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                        3)

        face_count = 0
        for i in range(0, len(res_fd[0][0])):
            if res_fd[0][0][i][2] > 0.7:
                face_count += 1

                xmin = int(initial_w * res_fd[0][0][i][3])
                ymin = int(initial_h * res_fd[0][0][i][4])
                xmax = int(initial_w * res_fd[0][0][i][5])
                ymax = int(initial_h * res_fd[0][0][i][6])
                confidence = int(res_fd[0][0][i][2] * 100) / 100

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (232, 35, 244), 4, 1)
                cv2.putText(frame, "Conf: " + str(confidence), (xmin + 5, ymin + 25), cv2.FONT_HERSHEY_COMPLEX , 1, (0, 255, 0), 2)
        if face_count > 1:
            cv2.putText(frame, "More than 1 face", (0 + 5, 0 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        else:
            try:
                face_frame = frame[ymin:ymax, xmin:xmax]
                face_frame_resize = cv2.resize(face_frame, (w_fr, h_fr))
                face_frame_resize = face_frame_resize.transpose((2, 0, 1))
                face_frame_resize = face_frame_resize.reshape((n_fr, c_fr, h_fr, w_fr))

                res_fr = exec_net2.infer(inputs = {input_blob_fr: face_frame_resize})
                res_fr = res_fr[out_blob_fr]
                frame_face_vector = res_fr[0][:].reshape(-1)
                similarity = -99
                index_of_i = -1
                for i in range(0, len(database_feature_list)):
                    val = np.frombuffer(database_feature_list[i][1], dtype=np.float32)

                    similarity_i_frame = np.dot(frame_face_vector, val) / (np.linalg.norm(frame_face_vector) * (np.linalg.norm(val)))
                    if similarity_i_frame > similarity:
                        similarity = similarity_i_frame
                        index_of_i = database_feature_list[i][0]

                index = index_of_i

                face_image_attribute = cv2.resize(face_frame, (w_fa, h_fa))
                face_image_attribute = face_image_attribute.transpose((2, 0, 1))

                res_fr = exec_net3.infer(inputs={input_blob_fa: face_image_attribute})

                gender = ''

                if res_fr["prob"][0][0][0][0] > res_fr["prob"][0][1][0][0]:
                    gender = 'Female'
                    conf = res_fr["prob"][0][0][0][0]
                else:
                    gender = 'Male'
                    conf = res_fr["prob"][0][1][0][0]

                cv2.putText(frame, "Age:" + str(int(res_fr["age_conv3"][0][0][0][0] * 100)), (5, 55),
                                cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 0, 0),2)
                cv2.putText(frame, "Gender:" + gender, (5, 85), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 0, 0),2)
                cv2.putText(frame, "Conf_" + gender + ":" + str(conf), (5, 115), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 0, 0),2)

                cv2.putText(frame, 'Similarity:%.2f' % (similarity), (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1,
                                        (0,0,0), 2)

                if similarity > 0.7:
                    person_name = database.database.find_person_name_by_person_id(index)

                    matched_face = cv2.imread('../database/images/' + person_name + '.jpg')

                    cv2.imshow("Detection Results", face_frame)
                    cv2.imshow('Matched Face', matched_face)
                    cv2.waitKey(5000)

                    break
            except:
                pass
        cv2.imshow("Detection Results", frame)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return False

    cap.release()
    cv2.destroyAllWindows()

    return person_name