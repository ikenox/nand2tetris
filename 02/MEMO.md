# 第2章 ブール算術

## やったこと

* 半加算器、全加算器、インクリメンタ、ALU（算術論理演算機）の実装

## メモ

* ALUを多機能にする（なるべくハードウェアで演算する）とパフォーマンスが良くなるが、コストは高くつく。
    * ALUとソフトウェアどちら側で演算を実装するかは、コストとパフォーマンスのトレードオフ

* 多ビットバスのピンの一部分のみ(ex. a[n], a[n..m] など)を利用したい場合は、多ビットバスのピンの出力時に分岐させておく必要がある。  
    * 入力時に多ビットバスのピンの一部分を指定するとエラーとなる

例:
```
// OK
Mux16 (a=pin16, b=false, sel=false, out=out, out[0..7]=out0to7, out[8..15]=out8to15); 
Or8Way (in=out0to7, out=or0to7);
Or8Way (in=out8to15, out=or8to15);

// ERROR
Mux16 (a=pin16, b=false, sel=false, out=out); 
Or8Way (in=out[0..7], out=or0to7);
Or8Way (in=out[8..15], out=or8to15);

```