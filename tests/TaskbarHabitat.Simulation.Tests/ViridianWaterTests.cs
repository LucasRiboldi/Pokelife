using TaskbarHabitat.Widget;

namespace TaskbarHabitat.Simulation.Tests;

public class ViridianWaterTests
{
    [Fact]
    public void WaterAdvancesAcrossBothRowsAndWrapsWithoutSkippingItsLastFrame()
    {
        Assert.Equal(new[] { 0, 0, 1, 3, 4, 7, 0, 2 },
            new[] { 0, 109, 110, 439, 440, 879, 880, 1100 }
                .Select(milliseconds => ViridianWater.FrameAt(TimeSpan.FromMilliseconds(milliseconds))));
    }
}
