ret, image = cap.read()

image_resized = np.array(image)
scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], 
                                                        feed_dict={tf_input: image_resized[None, ...]})
boxes = boxes[0] # index by 0 to remove batch dimension
scores = scores[0]
classes = classes[0]
num_detections = num_detections[0]


DETECTION_THRESHOLD = 0.5
# plot boxes exceeding score threshold
for i in range(int(num_detections)):
    if scores[i] < DETECTION_THRESHOLD:
        continue
    # scale box to image coordinates
    box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
    box  = box.astype(int)
    image = cv2.rectangle(image, (box[1], box[0]), (box[3], box[2]),(255,0,0),2)