# Linformer Pytorch Implementation
A practical implementation of the [Linformer paper](https://arxiv.org/pdf/2006.04768.pdf).

Has not been empirically tested (i.e. if it performs well on any datasets), but the self attention mechanism works.

I am not the author of the paper.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zHenqau3rMo3oS_7EisfGsahSs-1_sok?usp=sharing) 1.23m tokens

## How to use
Assuming you have `torch` installed from `pip`, and a GPU with enough memory:

```
git clone https://github.com/tatp22/linformer-pytorch.git
cd linformer-pytorch
python example.py
```

Copy the files into your project if need be. Will look into making this easily installable via `pip`.

Code Example:

```python
from linformer_pytorch import Linformer
import torch

device = torch.device("cuda")
model = Linformer(
        input_size=262144, # Dimension 1 of the input
        channels=64, # Dimension 2 of the input
        dim_d=256, # The inner dimension of the attention heads
        dim_k=128, # The second dimension of the P_bar matrix from the paper
        dim_ff=128, # Dimension in the feed forward network
        dropout_ff=0.15, # Dropout for feed forward network
        nhead=4, # Number of attention heads
        depth=2, # How many times to run the model
        dropout=0.1, # How much dropout to apply to P_bar after softmax
        activation="gelu", # What activation to use. Currently, only gelu and relu supported, and only on ff network.
        checkpoint_level="C0", # What checkpoint level to use. For more information, see below.
        ).cuda()
x = torch.randn(1, 262144, 64).cuda()
y = model(x)
print(y)
```

## Checkpoint levels
As an attempt to further introduce memory savings, the concept of checkpoint levels have been introduced. The current three checkpoint levels are `C0`, `C1`, and `C2`. When going up checkpoint levels, one sacrifices speed for memory savings. That is, checkpoint level `C0` is the fastest, but takes up the most space on the GPU, while `C2` is the slowest, but takes up the least space on the GPU. The details of each checkpoint level are as follows:
* `C0`: No checkpointing. The models runs while keeping all of the attention heads and ff layers in the GPU memory.
* `C1`: Checkpoint each MultiHead attention as well as each ff layer. With this, increasing `depth` should have minimal impact on the memory.
* `C2`: Along with the optimizations at the `C1` level, checkpoint each head in each MultiHead Attention layer. With this, increasing `nhead` should have minimal impact on the memory.

Performance details are still unknown, but the option exists for users that want to try.

## Padder
One slight problem with the current implementation of the Linformer is that your sequence length has to match the `input_size` flag of the model. The Padder, which is still a WIP, pads the input size, such that the tensor can be fed into the network.

## Practical Tips
* Note that the Linformer has O(nk) time and space complexity. So, while it may be linear in n, make sure that your k is not too large as well. These are editable with `input_size` and `dim_k`, respectively.
* Speaking about k, the authors found that empirical evidence supports the fact that "the performance of Linformer model is mainly determined by the projected dimension k instead of the ratio n/k". Therefore, even when increasing sequence lengths, it may be fine to keep a relatively low, constant k (the authors showed with k=256, that it still performed almost as good as a vanilla transformer).
* One more tip for k: The authors recommend that k = O(d/eps^2), if self attention wants to be approximated by full attention, with eps error.
* This code, so far, is pretty much only linear layers as well as matrix multiplications. So, libraries like `apex` should work with this, however, in practice, it has not been tested.
* In practice, I found that the memory and time requirements are more on the order of O(nkd), with n=`input_size`, k=`dim_k`, and d=`dim_d`.

## Future work
* ~~Change the `einsum`s to `matmul` for faster multiplication~~
* ~~Fix a bug where the model is using too much memory. Probably has to do with the inner dimension.~~
* Add positional embeddings
* Add option to change the `E` and `F` downsampling matrices
* Run some benchmark tests to see what the performance is
* Instead of matrix multiplication to bring the dimensions down to k (With EKW and FVW), try to do convolution, as mentioned in the paper, with a stride length and kernel size of n/k.
* In the paper, empirical studies showed that one can reduce the value of k when increasing depth. Add some option to decrease k more per layers, saving even more memory.

## Disclaimer
This is the first time that I am reproducing a result from a paper, so some things may be wrong. If you see a problem, please open up an issue, and I will attempt to work on it.

## Thanks
Thank you to [lucidrains](https://github.com/lucidrains), whose other sparse attention repositories helped me in designing this Linformer Repo.

## Citations

```bibtex
@misc{wang2020linformer,
    title={Linformer: Self-Attention with Linear Complexity},
    author={Sinong Wang and Belinda Z. Li and Madian Khabsa and Han Fang and Hao Ma},
    year={2020},
    eprint={2006.04768},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```
["Listen with attention..."](https://youtu.be/dRSOB-E0gPA?t=54)
