using System.Text.Json;

namespace TaskbarHabitat.Widget;

internal sealed class HabitatNavigation
{
    public readonly record struct Cell(int X, int Y);
    public sealed record Destination(Cell Cell, string Activity, bool Rest);
    private sealed record Map(int CellSize, string[] Rows, Cell Spawn, Destination[] Destinations);

    private readonly Map map;
    public int Columns => map.Rows[0].Length;
    public int Rows => map.Rows.Length;
    public int Width => Columns * map.CellSize;
    public int Height => Rows * map.CellSize;
    public Cell Spawn => map.Spawn;
    public IReadOnlyList<Destination> Destinations => map.Destinations;

    private HabitatNavigation(Map map) => this.map = map;

    public static HabitatNavigation Load(string path)
    {
        var map = JsonSerializer.Deserialize<Map>(File.ReadAllText(path), JsonSerializerOptions.Web);
        if (map is null || map.CellSize <= 0 || map.Rows is not { Length: > 0 } ||
            string.IsNullOrEmpty(map.Rows[0]) || map.Rows.Any(row =>
                row is null || row.Length != map.Rows[0].Length || row.Any(c => c is not ('.' or '#'))) ||
            map.Destinations is not { Length: > 0 })
            throw new InvalidDataException("A grade de caminhada é inválida.");

        var navigation = new HabitatNavigation(map);
        if (!navigation.IsFree(map.Spawn) || map.Destinations.Any(target =>
                target is null || !navigation.IsFree(target.Cell) || string.IsNullOrWhiteSpace(target.Activity)))
            throw new InvalidDataException("Viridian contém um destino de caminhada bloqueado ou inválido.");

        return navigation;
    }

    public (double X, double Y) Center(Cell cell) =>
        ((cell.X + 0.5) * map.CellSize, (cell.Y + 0.5) * map.CellSize);

    public bool IsFree(Cell cell) =>
        (uint)cell.Y < Rows && (uint)cell.X < Columns && map.Rows[cell.Y][cell.X] == '.';

    public Cell[] FindPath(Cell start, Cell goal)
    {
        if (!IsFree(start) || !IsFree(goal))
            return [];

        var costs = new int[Columns * Rows];
        var parents = new Cell[costs.Length];
        Array.Fill(costs, int.MaxValue);
        costs[Index(start)] = 0;
        var open = new PriorityQueue<(Cell Cell, int Cost), int>();
        open.Enqueue((start, 0), Estimate(start, goal));

        while (open.TryDequeue(out var entry, out _))
        {
            var current = entry.Cell;
            if (entry.Cost != costs[Index(current)])
                continue;
            if (current == goal)
                return Waypoints(start, goal, parents);

            for (int dy = -1; dy <= 1; dy++)
            for (int dx = -1; dx <= 1; dx++)
            {
                var neighbor = new Cell(current.X + dx, current.Y + dy);
                if (neighbor == current || !IsFree(neighbor))
                    continue;
                bool diagonal = dx != 0 && dy != 0;
                if (diagonal && (!IsFree(new Cell(neighbor.X, current.Y)) ||
                    !IsFree(new Cell(current.X, neighbor.Y))))
                    continue;

                int cost = entry.Cost + (diagonal ? 14 : 10);
                int index = Index(neighbor);
                if (cost >= costs[index])
                    continue;
                costs[index] = cost;
                parents[index] = current;
                open.Enqueue((neighbor, cost), cost + Estimate(neighbor, goal));
            }
        }

        return [];
    }

    private int Index(Cell cell) => cell.Y * Columns + cell.X;

    private static int Estimate(Cell from, Cell to)
    {
        int dx = Math.Abs(from.X - to.X);
        int dy = Math.Abs(from.Y - to.Y);
        return 10 * Math.Max(dx, dy) + 4 * Math.Min(dx, dy);
    }

    private Cell[] Waypoints(Cell start, Cell goal, Cell[] parents)
    {
        // Keep only turns so interpolation stays on the cells checked by A*.
        var path = new List<Cell> { goal };
        var direction = new Cell(0, 0);
        for (Cell current = goal; current != start;)
        {
            var parent = parents[Index(current)];
            var step = new Cell(current.X - parent.X, current.Y - parent.Y);
            if (step != direction && current != goal)
                path.Add(current);
            direction = step;
            current = parent;
        }
        if (start != goal)
            path.Add(start);
        path.Reverse();
        return [.. path];
    }
}
