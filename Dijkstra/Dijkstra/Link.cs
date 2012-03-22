using System;
using System.Collections.Generic;
using System.Linq;

namespace Dijkstra
{
    public struct Link
    {
        public int id1, id2;
        public double distance;

        public Link(int id1, int id2, double distance)
        {
            this.id1 = id1;
            this.id2 = id2;
            this.distance = distance;
        }

        public override string ToString()
        {
            return String.Format("({0}, {1}, {2})",
                                 id1,
                                 id2,
                                 distance); 
        }
    }
}
