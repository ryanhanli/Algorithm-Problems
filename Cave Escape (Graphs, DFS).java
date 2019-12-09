import java.io.*;
import java.util.*;

class Edge {
   int succ;
   Edge next;

   Edge(int succ, Edge next) {
      this.succ = succ;
      this.next = next;
   }
}

class Graph {
   Edge[] A; 
   // A[u] points to the head of a liked list;
   // p in the list corresponds to an edge u -> p.succ in the graph

   Graph(int n) {
      // initialize a graph with n vertices and no edges
      A = new Edge[n];
   }

   void addEdge(int u, int v) {
      // add an edge i -> j to the graph

      A[u] = new Edge(v, A[u]);
   }
}


// your "main program" should look something like this:
// def recDFS(u):
//     global color
//     color[u]=1
//     current = g.A[u]
//     global cyclic
//     global start
//     global end
//     while(current!=None):
//         succ = current.successor
//         if(color[succ]==1):
//             end = u
//             start = succ
//             cyclic = True
//             break
//         elif(color[succ]==0):
//             parent[succ]=u
//             recDFS(succ)
//             #global cyclic
//             if(cyclic):
//                 return
//         current = current.next
    
//     color[u]=2
    
// def DFS():
//     global cyclic
//     global color
//     for i in range(1,len(g.A)):
//         if(cyclic):
//             return
//         if(color[i]==0):
//             recDFS(i)

// def printcycle(start,end):
//     global string
//     #print(start)
//     #print(end)
//     if(end==start):
//         string+=(str(start) +" ")
//     else:
//         printcycle(start,parent[end])
//         string+=(str(end)+' ')
//         #print(string)
//     return string
public class DFSStarter {
   static Graph g; // global variable representing the graph

   static int[] colorArray; // global variable storing the color
                       // of each node during DFS: 
                       //    0 for white, 1 for gray, 2 for black

   static int[] parentArray;  // global variable representing the parent 
                         // of each node in the DFS forest
   static int first;
   static int last;
   static boolean hasCycle = false;
   static String final_string = "";
    
   static void recDFS(int u) {
      // perform a recursive DFS, starting at u
      // Took from slides so should work exactly as Shoup stated
       colorArray[u] = 1;
       Edge currentDFS = g.A[u];

        while(currentDFS!= null){

            int succ = currentDFS.succ;
            if(colorArray[succ]==0){
                parentArray[succ] = u;
                recDFS(succ);
                if(hasCycle){
                    return;
                }
            }
            else if(colorArray[succ] == 1){
                hasCycle = true;
                first = succ;
                last = u;
                break;
            }
            currentDFS = currentDFS.next; 
        }
        colorArray[u] = 2;
   }
//Took from slides as well
   static void DFS() {
        int limit = g.A.length;
        for(int i = 1; i< limit; i++) {
            if (hasCycle){ return; }
            if (colorArray[i] == 0) {
                recDFS(i);
            }
        }
   }
    
   static String firstCycle(int a, int z){
       if(z==a){
           final_string += a;
           final_string += " ";
       } else{
           firstCycle(a,parentArray[z]);
           final_string+= z;
           final_string+=" ";
       }
       return final_string;
   }

   public static void main(String[] args) {
       Scanner scanner = new Scanner(System.in);
       String[] initialInput= scanner.nextLine().split(" ");
       
       int vertices = Integer.parseInt(initialInput[0]);
       int edges = Integer.parseInt(initialInput[1]);
       vertices++;
       edges++;
       g = new Graph(vertices);
       parentArray = new int[vertices];
       colorArray = new int[vertices];
// for line in fileinput.input():
//     inputlist.append(line.strip())
// #print(inputlist)
// holder = inputlist[0].split()
// room_number = (int)(holder[0])
// edge_number = (int)(holder[1])
// inputlist.pop(0)
// #print(inputlist)

// g = Graph(room_number+1)
// color = [0]*(room_number+1)
// parent = [None]*(room_number+1)
// #A = [None]*(room_number+1)

// for edge in inputlist:
//     edge=edge.split()
//     source = (int)(edge[0])
//     destination = (int)(edge[1])
//     g.addEdge(source, destination)
//     #print(g.A)
    

// DFS()
// if(cyclic==False):
//     print(0)
// else:
//     print(1)
//     print(printcycle(start,end))
       for (int i=0;i<edges-1;i++){
           String[] edgeInput = scanner.nextLine().split(" ");
           int source = Integer.parseInt(edgeInput[0]);
           int destination = Integer.parseInt(edgeInput[1]);
           g.addEdge(source,destination);
       }
       for(int i: colorArray) { i = 0;  } 
       DFS();
       if(hasCycle){
           System.out.println("1");
           System.out.println(firstCycle(first,last));
       } else{
           System.out.println("0");
       }
       
   }

}
