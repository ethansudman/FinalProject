using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace Dijkstra
{
    class Program
    {
        static void Main(string[] args)
        {
            // todo: almost right except first one
            Console.WriteLine("Single:");
            Single();
            
            Console.WriteLine();
            Console.Write("Double:");
            Double();

            Console.ReadLine();
        }

        /// <summary>
        /// Tests the sequential version of this program
        /// </summary>
        private static void Single()
        {
            List<Link> results = Dijkstra(getGraph(), 0);

            foreach (Link link in results) Console.WriteLine(link);
        }

        /// <summary>
        /// Tests the parallel version of this program
        /// </summary>
        private static void Double()
        {
            List<Link> results = Dijkstra_p(getGraph(), 0);

            foreach (Link link in results) Console.WriteLine(link);
        }

        /// <summary>
        /// Generate a sample <see cref="Graph"/>
        /// </summary>
        /// 
        /// <returns>
        /// Sample <see cref="Graph"/>
        /// </returns>
        private static Graph getGraph()
        {
            List<int> vertices = new List<int>() { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
            List<Link> links = new List<Link>();

            foreach (int i in vertices)
            {
                foreach (int j in vertices)
                {
                    double dist = Math.Abs(Math.Sin(i + j + 1));
                    Link link = new Link(i, j, dist);
                    links.Add(link);
                }
            }

            return new Graph(links, vertices);
        }

        /// <summary>
        /// Sequential version
        /// </summary>
        /// 
        /// <param name="graph">
        /// <see cref="Graph"/> object to check the path for
        /// </param>
        /// 
        /// <param name="start">
        /// Start
        /// </param>
        /// 
        /// <returns>
        /// List of <see cref="Link"/> objects
        /// </returns>
        private static List<Link> Dijkstra(Graph graph, int start)
        {
            List<Vertex> P =
                (from v in graph.Vertices
                 select new Vertex(v, graph.Links)).ToList();
            
            var qT =
                from vertex in P
                where vertex.ID != start
                orderby vertex.ID ascending
                select vertex;

            Queue<Vertex> Q = new Queue<Vertex>(qT);

            Vertex curr = P[start];
            curr.closest_distance = 0.0f;

            while (Q.Count > 0)
            {
                foreach (Tuple<int, double> n in curr.neighbors)
                {
                    Vertex neighbor = P[n.Item1];
                    double dist = n.Item2 + curr.closest_distance;

                    bool contains = (from v in Q where v.ID == n.Item1 select v).Count() > 0;

                    if (contains && (dist < neighbor.closest_distance))
                    {
                        neighbor.closest = curr;
                        neighbor.closest_distance = dist;
                    }
                }

                curr = Q.Dequeue();
            }

            return
                (from v in P
                 where v.ID != start
                 select new Link(v.ID, v.closest.ID, v.closest_distance)).ToList();
        }

        /// <summary>
        /// Parallel Dijkstra algorithm
        /// </summary>
        /// 
        /// <param name="graph">
        /// <see cref="Graph"/> object to check the path for
        /// </param>
        /// 
        /// <param name="start">
        /// Start
        /// </param>
        /// 
        /// <returns>
        /// List of <see cref="Link"/> objects
        /// </returns>
        private static List<Link> Dijkstra_p(Graph graph, int start)
        {
            List<Vertex> P =
                (from v in graph.Vertices
                 select new Vertex(v, graph.Links)).ToList();

            var qT =
                from vertex in P
                where vertex.ID != start
                orderby vertex.ID ascending
                select vertex;

            Queue<Vertex> Q = new Queue<Vertex>(qT);

            Vertex curr = P[start];
            curr.closest_distance = 0.0f;

            while (Q.Count > 0)
            {
                Barrier barrier = new Barrier(curr.neighbors.Count + 1);

                foreach (Tuple<int, double> n in curr.neighbors)
                {
                    var tuple = n;
                    ThreadPool.QueueUserWorkItem(
                        obj =>
                        {
                            Vertex neighbor = P[tuple.Item1];
                            double dist = tuple.Item2 + curr.closest_distance;

                            bool contains = (from v in Q where v.ID == tuple.Item1 select v).Count() > 0;

                            if (contains && (dist < neighbor.closest_distance))
                            {
                                neighbor.closest = curr;
                                neighbor.closest_distance = dist;
                            }

                            barrier.SignalAndWait();
                        },
                        null);
                }

                barrier.SignalAndWait();

                barrier.Dispose();

                curr = Q.Dequeue();
            }

            return
                (from v in P
                 where v.ID != start
                 select new Link(v.ID, v.closest.ID, v.closest_distance)).ToList();
        }
    }
}
