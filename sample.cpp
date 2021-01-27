#include <bits/stdc++.h>

using namespace std;

// Complete the encryption function below.
string encryption(string s) {
float len;
int row,col,j=0;
string sDup;
for(int i=0;s[i]!='\0';++i)
{   if(s[i]!=32)
    {
        sDup[j]=s[i];
        j++;
    }
}
/*for(int i=0;s[i]!='\0';++i)
{
    cout<<sDup[i];
}*/
len=j;
row=floor(sqrt(len));
col=ceil(sqrt(len));
//cout<<row<<col<<' '<<len;
string res;
int k=0,index=0;
j=0;
int m=0;
while(k<=col)
{
    while(j<len)
    {
        res[index]=sDup[j];
        j=j+col;
        index++;
    }
    res[index]=32;
    //index++;
    k++;
    j=0;
    m=m+1;
    j=m;
}
for(int i=0;i<len;++i)
    cout<<res[i];


return(res);
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    string s;
    getline(cin, s);

    string result = encryption(s);

    fout << result << "\n";

    fout.close();

    return 0;
}
