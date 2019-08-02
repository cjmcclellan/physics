# --The configuration file for Physics----------


# --Tensorflow Flags------------------
tf_flag = True
try:
    import tensorflow as tf
    tf_dtype = tf.float32

except:
    tf_flag = False


