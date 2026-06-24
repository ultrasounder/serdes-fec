module blink(
    input wire clk, 
    input wire rst,
    output reg q
);
always @(posedge clk)
if (rst) q <= 1'b0;
else q<= ~q;
endmodule
