//PRBS: polynomial x^7 + x^6 + 1, period 2^7 - 1 = 127
module prbs7 (
    input wire clk,
    input wire rst,
    input wire en,
    output wire out

);

reg [6:0] lfsr;
wire fb = lfsr[6] ^ lfsr[5]; //taps 7 and 6 (0-indexed: 6 and 5)

always @(posedge clk) begin
    if(rst) lfsr <= 7'h7F; //nonzero seed (all-ones)
    else if (en) lfsr <= {lfsr[5:0], fb};
end

assign out = lfsr[6];

endmodule 