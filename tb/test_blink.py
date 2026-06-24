import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_blink_toggles(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    dut.rst.value = 1
    await RisingEdge(dut.clk); await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    prev = int(dut.q.value)
    for _ in range(8):
        await RisingEdge(dut.clk)
        cur = int(dut.q.value)
        assert cur != prev, "q failed to toggle"
        prev = cur