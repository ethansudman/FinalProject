using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Dijkstra
{
    public sealed class Vertex
    {
        private readonly int id;
        private readonly List<Tuple<int, double>> _neighbors;

        public Vertex closest
        {
            get;
            set;
        }

        public double closest_distance
        {
            get;
            set;
        }

        public int ID
        {
            get { return id; }
        }

        public List<Tuple<int, double>> neighbors
        {
            get { return _neighbors; }
        }

        public Vertex(int id, List<Link> links)
        {
            this.id = id;
            closest = null;
            closest_distance = double.PositiveInfinity;

            _neighbors = new List<Tuple<int, double>>();

            foreach (Link link in links)
            {
                if (link.id1 == id)
                {
                    Tuple<int, double> tuple = new Tuple<int, double>(link.id2, link.distance);
                    _neighbors.Add(tuple);
                }
            }
        }
    }
}