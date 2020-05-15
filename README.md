# Network Security - Merkle Tree

This is a code for a functional Merkle Tree. 

In this project we:

1) Create a Merkle Tree.
2) Generate a Proof Of Inclusion to a given node in the tree.
3) Check the Validation of a given node, root and Proof Of Inclusion.
4) Use "Brute Force" to find a valid hashed expression for a given difficult level.

## Details
There are 4 different commands in this code, 1-4 as explained above.
Examples:
This command will create a new Merkle Tree with 4 members:
```bash
1 a b c d
```
The output is the root of the new tree:
```bash
12a40550c10c6339bf6f271445270e49b844d6c9e8abc36b9b642be532befe94
```
This command will generate a Proof Of Inclusion for the member in the 1st position (the count starts at 0):
```bash
2 1
```
The output will be the Proof of inclusion:
```bash
l a r 21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4
```
This command will check if the member **b** is a Merkle Tree with a root of **12a40550c10c6339bf6f271445270e49b844d6c9e8abc36b9b642be532befe94**, and a Proof Of Inclusion of **l a r 21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4**
(The returned value is True/False):
```bash
3 b 12a40550c10c6339bf6f271445270e49b844d6c9e8abc36b9b642be532befe94 l a r 21e721c35a5823fdb452fa2f9f0a612c74fb952e06927489c6b27a43b817bed4
```
output:
```bash
True
```
This command will look for the first appearance of a hash with a given amount of zeros at the start of the hash. The hash will be built with i (an increasing number) and the root of the Merkle Tree appended to it. We iterate with i until we get a hash with the at least **n** leading zeors.
The input : 
```bash
4 2
```
will give us (**at least** 2 zeros at the start):
```bash
296 00038effdfc87247806ade69b932b51697490a9f9479ed43aef31657169e8703
```
296 is the number of iterations.
