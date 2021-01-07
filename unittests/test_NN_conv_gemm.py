"""
Unitary tests for NN_gemm_conv.py.

For running all the tests quietly, execute from the parent directory:
    python -m unittest unittests.TestConvGemm

For running all the tests verbosely, execute from the parent directory:
    python -m unittest -v unittests.TestConvGemm

For running an individual test verbosely, execute from the parent directory:
    python -m unittest -v unittests.TestConvGemm.test_name
"""

import inspect
import math
import sys
import unittest

import numpy as np

from .tools import Spinner

try:
    from NN_conv_gemm import ConvGemm
    from NN_im2col_cython import im2col_cython
except ModuleNotFoundError:
    print("Please, execute as 'python -m unittest unittests.TestConvGemm'")


def verbose():
    """Returns True if unittest has been called with -v or --verbose options."""
    return '-v' in sys.argv or '--verbose' in sys.argv


class D:
    """Default parameters"""
    b = 1  # Batch size
    c = 1  # Channels per layer
    h = 128  # Layers height
    w = 100  # Layers width
    kn = 1  # Number of filters
    kh = 16  # Filters weights height
    kw = 10  # Filters weights width
    vpadding = 1  # Vertical padding
    hpadding = 2  # Horizontal padding
    vstride = 1  # Vertical stride
    hstride = 1  # Horizontal stride


def _print_with_header(header, to_be_printed):
    print("-" * (len(header) + 2))
    print(" {}".format(header))
    print("-" * (len(header) + 2))
    if to_be_printed is not None:
        print(to_be_printed)


def _conv_gemm_and_im2col_mm(weights, x, biases=None, vpadding=0, hpadding=0, vstride=1, hstride=1):
    if verbose():
        print()
    kn, ck, kh, kw = weights.shape
    # b, c, h, w = x.shape
    conv_gemm = ConvGemm(debug=verbose())
    conv_gemm_result = conv_gemm.conv_gemm(weights, x, biases=biases,
                                           vpadding=vpadding, hpadding=hpadding,
                                           vstride=vstride, hstride=hstride)
    x_c = im2col_cython(x, kh, kw, vpadding, hpadding, vstride, hstride)
    w_c = weights.reshape(kn, -1)
    if biases is None:
        im2col_mm_result = w_c @ x_c
    else:
        im2col_mm_result = w_c @ x_c + biases
    if verbose():
        _print_with_header("{} conv_gemm_result".format(inspect.stack()[1][3]), conv_gemm_result)
        print("Shape: ", conv_gemm_result.shape,
              " Sum: ", conv_gemm_result.sum(),
              " Min: ", conv_gemm_result.min(),
              " Max: ", conv_gemm_result.max())
        _print_with_header("{} im2col_mm_result".format(inspect.stack()[1][3]), im2col_mm_result)
        print("Shape: ", im2col_mm_result.shape,
              " Sum: ", im2col_mm_result.sum(),
              " Min: ", im2col_mm_result.min(),
              " Max: ", im2col_mm_result.max())
        print("---")
        print("Maximum difference: ",
              max([abs(x - y) for x, y in zip(conv_gemm_result.flatten(), im2col_mm_result.flatten())]))
        print("---")
    return conv_gemm_result, im2col_mm_result


class TestConvGemm(unittest.TestCase):
    """
    Tests that conv_gemm leads to the same results than i2c and mm.
    """

    # @delete: different strides are now supported
    # def test_raise_on_different_strides(self):
    #     x = np.ones((D.b, D.c, D.h, D.w)).astype(np.float32, order='C')
    #     weights = np.ones((D.kn, D.c, D.kh, D.kw)).astype(np.float32, order='C')
    #     conv_gemm = ConvGemm(debug=verbose())
    #     with self.assertRaises(AssertionError):
    #         conv_gemm.conv_gemm(weights, x, vstride=1, hstride=2)

    def test_handmade_array(self):
        """
        Test that manual matrices lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]]]]).astype(np.float32, order='C')
        weights = np.array([[[[1, 1],
                              [1, 1]]]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_handmade_array_kn_2(self):
        """
        Test that manual matrices with kn = 2 lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]]]]).astype(np.float32, order='C')
        weights = np.array([[[[1, 1],
                              [1, 1]]],
                            [[[2, 2],
                              [2, 2]]]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_handmade_array_kn_2_c_2(self):
        """
        Test that manual matrices with kn = 2 lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]],
                       [[1, 2, 4, 8],
                        [16, 32, 64, 128]]]]).astype(np.float32, order='C')
        weights = np.array([[[[1, 2],
                              [4, 8]],
                             [[2, 2],
                              [2, 2]]],
                            [[[4, 4],
                              [4, 4]],
                             [[8, 8],
                              [8, 8]]]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_handmade_array_with_biases(self):
        """
        Test that manual matrices including b lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]]]]).astype(np.float32, order='C')
        weights = np.array([[[[1, 1],
                              [1, 1]]]]).astype(np.float32, order='C')
        biases = np.array([[1024, 2048, 4196]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x, biases=biases,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_larger_handmade_array(self):
        """
        Test that larger manual matrices lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]],
                       [[128, 256, 512, 1024],
                        [2048, 4096, 8192, 16384]]]]).astype(np.float32, order='C')
        weights = np.array([[[[1, 2],
                              [3, 4]],
                             [[4, 5],
                              [6, 7]],
                             ]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_even_larger_handmade_array(self):
        """
        Test that even larger manual matrices lead to the same solution
        """
        x = np.array([[[[1, 2, 4, 8],
                        [16, 32, 64, 128]],
                       [[128, 256, 512, 1024],
                        [2048, 4096, 8192, 16384]]],
                      [[[1, 2, 4, 8],
                        [16, 32, 64, 128]],
                       [[128, 256, 512, 1024],
                        [2048, 4096, 8192, 16384]]],
                      ]).astype(np.float32, order='C')
        weights = np.array([[[[1, 1],
                              [1, 1]],
                             [[4, 4],
                              [4, 4]]]]).astype(np.float32, order='C')
        padding = 0
        stride = 1
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=padding, hpadding=padding,
                                                                      vstride=stride, hstride=stride)
        if verbose():
            print(["{:b}  ".format(int(x)) for x in conv_gemm_result.ravel()])
            print(["{:b}  ".format(int(x)) for x in im2col_mm_result.ravel()])
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_defaults_with_ones(self):
        """
        Test that the default parameters on ones matrices lead to the same solution
        """
        weights = np.ones((D.kn, D.c, D.kh, D.kw)).astype(np.float32, order='C')
        x = np.ones((D.b, D.c, D.h, D.w)).astype(np.float32, order='C')
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=D.vpadding, hpadding=D.hpadding,
                                                                      vstride=D.vstride, hstride=D.hstride)
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_defaults_with_random(self):
        """
        Test that the default parameters on random matrices lead to the same solution
        """
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x,
                                                                      vpadding=D.vpadding, hpadding=D.hpadding,
                                                                      vstride=D.vstride, hstride=D.hstride)
        # if verbose():
        #     print("Result[0, 0, 0, 1]=")
        #     partial_l = x[0, 0, 0:D.kh, 1:D.kw+1].flatten()
        #     print(w.flatten() @ partial_l)
        #     print("Result[0, 0, 0, 2]=")
        #     partial_l = x[0, 0, 0:D.kh, 2:D.kw+2].flatten()
        #     print(w.flatten() @ partial_l)
        #     print("Result[0, 0, 1, 0]=")
        #     partial_l = x[0, 0, 1:D.kh+1, 0:D.kw].flatten()
        #     print(w.flatten() @ partial_l)

        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_defaults_including_biases_with_random(self):
        """
        Test that the default parameters on random matrices, including b, lead to the same solution
        """
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        ho = int(math.floor((D.h + 2 * D.vpadding - D.kh) / D.vstride + 1))
        wo = int(math.floor((D.w + 2 * D.hpadding - D.kw) / D.hstride + 1))
        biases = np.random.rand(D.kn, D.b * ho * wo).astype(np.float32, order='C')
        conv_gemm_result, im2col_mm_result = _conv_gemm_and_im2col_mm(weights, x, biases=biases,
                                                                      vpadding=D.vpadding, hpadding=D.hpadding,
                                                                      vstride=D.vstride, hstride=D.hstride)
        self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result))

    def test_with_different_kn(self):
        spinner = Spinner()
        if verbose():
            _print_with_header("{}".format(inspect.stack()[1][3]), None)
            print(" kn   Maximum difference    sum(cg_result)")
            print("----+--------------------+-----------------")
        conv_gemm = ConvGemm(debug=False)
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        np_all_close_for_all_cases = True
        for kn in range(1, 32):
            if not verbose():
                spinner.render()
            weights = np.random.rand(kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
            conv_gemm_result = conv_gemm.conv_gemm(weights, x,
                                                   vpadding=D.vpadding, hpadding=D.hpadding,
                                                   vstride=D.vstride, hstride=D.hstride)
            x_c = im2col_cython(x, D.kh, D.kw, D.vpadding, D.hpadding, D.vstride, D.hstride)
            w_c = weights.reshape(kn, -1)
            im2col_mm_result = w_c @ x_c
            if verbose():
                print("{:3}    {:9.7f}             {:11.2f}"
                      "".format(kn, max([abs(x - y) for x, y in zip(conv_gemm_result.flatten(),
                                                                    im2col_mm_result.flatten())]),
                                np.sum(conv_gemm_result)))
            np_all_close_for_all_cases = np_all_close_for_all_cases and np.allclose(conv_gemm_result, im2col_mm_result)
        if not verbose():
            spinner.stop()
        self.assertTrue(np_all_close_for_all_cases)

    def test_with_different_b(self):
        spinner = Spinner()
        if verbose():
            _print_with_header("{}".format(inspect.stack()[1][3]), None)
            print("  b   Maximum difference")
            print("----+--------------------")
        conv_gemm = ConvGemm(debug=False)
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        np_all_close_for_all_cases = True
        for b in range(1, 32):
            if not verbose():
                spinner.render()
            x = np.random.rand(b, D.c, D.h, D.w).astype(np.float32, order='C')
            conv_gemm_result = conv_gemm.conv_gemm(weights, x,
                                                   vpadding=D.vpadding, hpadding=D.hpadding,
                                                   vstride=D.vstride, hstride=D.hstride)
            x_c = im2col_cython(x, D.kh, D.kw, D.vpadding, D.hpadding, D.vstride, D.hstride)
            w_c = weights.reshape(D.kn, -1)
            im2col_mm_result = w_c @ x_c
            if verbose():
                print("{:3}    {:9.7f}".format(b,
                                               max([abs(x - y) for x, y
                                                    in zip(conv_gemm_result.flatten(), im2col_mm_result.flatten())])))
            np_all_close_for_all_cases = np_all_close_for_all_cases and np.allclose(conv_gemm_result, im2col_mm_result)
        if not verbose():
            spinner.stop()
        self.assertTrue(np_all_close_for_all_cases)

    def test_with_different_padding(self):
        spinner = Spinner()
        if verbose():
            _print_with_header("{}".format(inspect.stack()[1][3]), None)
            print("  p   Maximum difference")
            print("----+--------------------")
        conv_gemm = ConvGemm(debug=False)
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        np_all_close_for_all_cases = True
        for padding in range(0, 5):
            if not verbose():
                spinner.render()
            conv_gemm_result = conv_gemm.conv_gemm(weights, x,
                                                   vpadding=padding, hpadding=padding,
                                                   vstride=D.vstride, hstride=D.hstride)
            x_c = im2col_cython(x, D.kh, D.kw, padding, padding, D.vstride, D.hstride)
            w_c = weights.reshape(D.kn, -1)
            im2col_mm_result = w_c @ x_c
            if verbose():
                print("{:3}    {:9.7f}".format(padding,
                                               max([abs(x - y) for x, y
                                                    in zip(conv_gemm_result.flatten(), im2col_mm_result.flatten())])))
            np_all_close_for_all_cases = np_all_close_for_all_cases and np.allclose(conv_gemm_result, im2col_mm_result)
        if not verbose():
            spinner.stop()
        self.assertTrue(np_all_close_for_all_cases)

    def test_with_different_stride(self):
        spinner = Spinner()
        if verbose():
            _print_with_header("{}".format(inspect.stack()[1][3]), None)
            print("  s   Maximum difference")
            print("----+--------------------")
        conv_gemm = ConvGemm(debug=False)
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        np_all_close_for_all_cases = True
        for stride in range(1, 6):
            if not verbose():
                spinner.render()
            conv_gemm_result = conv_gemm.conv_gemm(weights, x,
                                                   vpadding=D.vpadding, hpadding=D.hpadding,
                                                   vstride=stride, hstride=stride)
            x_c = im2col_cython(x, D.kh, D.kw, D.vpadding, D.hpadding, stride, stride)
            w_c = weights.reshape(D.kn, -1)
            im2col_mm_result = w_c @ x_c
            if verbose():
                print("{:3}    {:9.7f}".format(stride,
                                               max([abs(x - y) for x, y
                                                    in zip(conv_gemm_result.flatten(), im2col_mm_result.flatten())])))
            np_all_close_for_all_cases = np_all_close_for_all_cases and np.allclose(conv_gemm_result, im2col_mm_result)
        if not verbose():
            spinner.stop()
        self.assertTrue(np_all_close_for_all_cases)

    def test_with_different_strides(self):
        spinner = Spinner()
        if verbose():
            _print_with_header("{}".format(inspect.stack()[1][3]), None)
            print(" vs  hs   Maximum difference")
            print("--------+--------------------")
        conv_gemm = ConvGemm(debug=False)
        weights = np.random.rand(D.kn, D.c, D.kh, D.kw).astype(np.float32, order='C')
        x = np.random.rand(D.b, D.c, D.h, D.w).astype(np.float32, order='C')
        for vstride in range(1, 5):
            for hstride in range(1, 5):
                if vstride == hstride:
                    continue
                if not verbose():
                    spinner.render()
                conv_gemm_result = conv_gemm.conv_gemm(weights, x,
                                                       vpadding=D.vpadding, hpadding=D.hpadding,
                                                       vstride=vstride, hstride=hstride)
                x_c = im2col_cython(x, D.kh, D.kw, D.vpadding, D.hpadding, vstride, hstride)
                w_c = weights.reshape(D.kn, -1)
                im2col_mm_result = w_c @ x_c
                if verbose():
                    print("{:3} {:3}    {:9.7f}".format(vstride, hstride,
                                                        max([abs(x - y) for x, y
                                                             in
                                                             zip(conv_gemm_result.flatten(),
                                                                 im2col_mm_result.flatten())])))
                self.assertTrue(np.allclose(conv_gemm_result, im2col_mm_result),
                                f"Results differ with vstride {vstride} and hstride {hstride}")
        if not verbose():
            spinner.stop()


if __name__ == '__main__':
    try:
        ConvGemm()
    except NameError:
        sys.exit(-1)
    unittest.main()
