import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_prbs7_period(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    dut.en.value = 1
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    
    bits = []
    
    for _ in range(254):
        await RisingEdge(dut.clk)
        bits.append(int(dut.out.value))
        
    # period-127: second half must equal first half
    first, second = bits[:127], bits[127:254]
    assert first == second, "PRBS7 period != 127"
    
    # sanity: not stuck, both symbols appear
    assert 0 < sum(first) < 127, "LFSR stuck at constant"
    dut._log.info(f"PRBS7 OK: period 127, ones={sum(first)}/127")