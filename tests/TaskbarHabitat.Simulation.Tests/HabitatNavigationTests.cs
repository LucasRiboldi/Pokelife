using TaskbarHabitat.Widget;
using Cell = TaskbarHabitat.Widget.HabitatNavigation.Cell;

namespace TaskbarHabitat.Simulation.Tests;

public sealed class HabitatNavigationTests
{
    [Fact]
    public void ViridianRoutesReachEveryLandmarkWithoutCrossingBlockedCells()
    {
        var grid = HabitatNavigation.Load(Path.Combine(AppContext.BaseDirectory, "viridian-navigation.json"));
        Assert.Equal((1536, 1024), (grid.Width, grid.Height));

        var river = new Cell(118, 69);
        var roots = new Cell(96, 98);
        var behindCanopy = new Cell(97, 80);
        var eastBank = new Cell(145, 90);
        Assert.False(grid.IsFree(river));
        Assert.False(grid.IsFree(roots));
        Assert.True(grid.IsFree(behindCanopy));
        Assert.True(grid.IsFree(eastBank));
        Assert.Empty(grid.FindPath(grid.Spawn, eastBank));
        Assert.Contains(grid.Destinations, target => target.Cell == behindCanopy);

        var start = grid.Spawn;
        foreach (var target in grid.Destinations.Append(grid.Destinations[0]))
        {
            var path = grid.FindPath(start, target.Cell);
            Assert.True(path.Length > 1, target.Activity);
            Assert.Equal(start, path[0]);
            Assert.Equal(target.Cell, path[^1]);
            for (int i = 1; i < path.Length; i++)
            {
                Cell cell = path[i - 1];
                Cell next = path[i];
                int dx = next.X - cell.X;
                int dy = next.Y - cell.Y;
                Assert.True(dx == 0 || dy == 0 || Math.Abs(dx) == Math.Abs(dy));
                while (cell != next)
                {
                    var step = new Cell(cell.X + Math.Sign(dx), cell.Y + Math.Sign(dy));
                    Assert.True(grid.IsFree(step));
                    if (dx != 0 && dy != 0)
                    {
                        Assert.True(grid.IsFree(new Cell(step.X, cell.Y)));
                        Assert.True(grid.IsFree(new Cell(cell.X, step.Y)));
                    }
                    cell = step;
                }
            }
            start = target.Cell;
        }
    }
}
