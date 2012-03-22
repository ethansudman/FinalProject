using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Dijkstra
{
    public sealed class Graph
    {
        private readonly List<Link> links;
        private readonly List<int> vertices;

        public List<Link> Links
        {
            get { return links; }
        }

        public List<int> Vertices
        {
            get { return vertices; }
        }

        public Graph(List<Link> links, List<int> vertices)
        {
            this.links = links;
            this.vertices = vertices;
        }
    }
}
