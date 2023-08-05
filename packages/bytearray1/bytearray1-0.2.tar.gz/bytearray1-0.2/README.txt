## Installation

Run the following to install:

```python3
pip3 install bytearray1
```


```python
pip install bytearray1
```

## Usage

```python
import bytearray1

t = bytearray1.ByteArray()
t.writeUTF('code')
t.writeByte(1)
t.writeInt(76)
t.writeShort(4)
output = t.toByteArray()

b = bytearray1.ByteArray(output)
type = b.readUTF()
true = b.readByte()
y = b.readInt()
x = b.readShort()
```