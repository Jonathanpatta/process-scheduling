#include<iostream>
#include<queue>
#include<stdio.h>

using namespace std;

struct p_data
{
    string pid;
    int bursttime;
    int arrivaltime;
};

queue<p_data> q;
vector<p_data> qt;

void enter_data(struct p_data *l)
{
    int i;
    printf("enterpid of process :");cin>>l->pid;
    printf("bursttime of process :");scanf("%d",&l->bursttime);
    printf("arrivaltime of process :");scanf("%d",&l->arrivaltime);

}

void showv(vector<p_data> &vect)
{
    cout<<"    vector:";
    for (int i=0; i<vect.size(); i++)
       cout << vect[i].pid << " ";
}

void showq(queue <p_data> gq)
{
	queue <p_data> g = gq;
	cout<<"queue state:  ";
	while (!g.empty())
	{
		cout << "|pid:" << g.front().pid<<" , bt:"<<g.front().bursttime<< "|";
		g.pop();
	}
	cout << '\n';
}

int minat(vector<p_data> g)
{
	int m=1000;
	for(int i=0;i<g.size();i++)
	{
		if(g[i].arrivaltime<m)
        {
            m=g[i].arrivaltime;
        }

	}
	return m;
}

int findmin(int t)
{
    for(int i=0;i<qt.size();i++)
    {
        if(qt[i].arrivaltime==t)
            return i;
    }
}

void load_queue(queue <p_data> &q,vector<p_data> &v,int c,int t)
{
    int a[100];
    int n=0;
    for(int i=0;i<v.size();i++)
    {
        if(v[i].arrivaltime<=c&&v[i].arrivaltime>c-t)
        {
            q.push(v[i]);
            a[n]=i;
            n++;
            //v.erase( v. begin() + i );
            //i--;
        }
    }
    for(int i=0;i<n;i++)
    {
        v.erase( v. begin() + a[i] );
    }
    //return n;
    //showv(v);
}



int main()
{

    int i;
    int time_quantum=2;
    int total;
    int num=4;
    for(i=0;i<num;i++)
    {
        p_data *l = new p_data;
        enter_data(l);
        //qt.push_back(*l);
        if(l->arrivaltime==0){
            q.push(*l);
            total++;
        }
        //else
            qt.push_back(*l);
    }
    cout<<"\n\n";
    int time=0;
    //int m=maxat(qt);

    while(!q.empty())
    {

        cout<<"time:"<<time<<"   \t";
        showv(qt);
        showq(q);
        time+=time_quantum;
        //load_queue(q,qt,time,time_quantum);

        if(q.front().bursttime<time_quantum)
        {
            q.front().bursttime=0;
            q.pop();
        }
        else
        {
            q.front().bursttime-=time_quantum;
            p_data t=q.front();
            q.pop();
            load_queue(q,qt,time,time_quantum);
            q.push(t);
        }


        cout<<"\n";
        //load_queue(q,qt,time,time_quantum);
    }

	return 0;
}
