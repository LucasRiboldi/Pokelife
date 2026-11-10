using TaskbarHabitat.Widget;

namespace TaskbarHabitat.Simulation.Tests;

public class CharmanderAnimationTests
{
    [Fact]
    public void WalkingUsesFourPosesPerStrideAndSelectsTheViewFromTheTrail()
    {
        Assert.Equal(new[] { 4, 5, 6, 7, 4 },
            new[] { 0, 2, 4, 6, 8 }.Select(distance => CharmanderAnimation.WalkFrame(-12, 2, distance)));
        Assert.Equal(0, CharmanderAnimation.WalkFrame(2, 10, 0));
        Assert.Equal(8, CharmanderAnimation.WalkFrame(2, -10, 0));
    }

    [Fact]
    public void GrassPauseSettlesBreathesAndStandsBeforeWalkingAgain()
    {
        Assert.Equal(new int?[] { 12, 15, 16, 17, 18, 19, 18, 17, 16, 15, 12, null },
            new[] { 0, .25, .65, 1.35, 1.65, 2.25, 2.85, 4.1, 4.45, 4.75, 5.05, 5.35 }
                .Select(CharmanderAnimation.RestFrame));
    }
}
