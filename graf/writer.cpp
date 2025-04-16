#include <fstream>
#include <iostream>
#include <ostream>
#include <vector>

using namespace std;

int main()
{
  ifstream data;
  data.open("data.txt");

  if ( !data.is_open() )
  {
    cout << "Error open data file!" << endl;
  }


}
