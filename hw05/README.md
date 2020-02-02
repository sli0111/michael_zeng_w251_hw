1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
2. What is TensorRT? How is it different from TensorFlow?
3. What is ImageNet? How many images does it contain? How many classes?
4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
5. In your own words, what is a bottleneck?
6. How is a bottleneck different from the concept of layer freezing?
7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
8. How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
9. How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? 11. Were you able to train it using a few images, or did you need a lot?
12. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
13. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?
14. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?