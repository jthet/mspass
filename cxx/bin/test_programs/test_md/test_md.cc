#include "Metadata.h"
#include "AntelopePf.h"
using namespace mspass;
int main(int argc, char **argv)
{
	//string pfname("test_md");
	char *pfname=strdup("test_md");
	int ierr;
	try {
		cout << "Trying to build Metadata objects" << endl;
		cout << "Trying default constructor" << endl;
		Metadata mdplain;
                cout << "Trying put methods for int, double, string, and bool"
                    <<endl;
                long lval; double dval; string sval;  bool bval;
                lval=10;
                mdplain.put<long>("long_val",lval);
                dval=2.5;
                mdplain.put<double>("double_val",dval);
                sval=string("test_string");
                mdplain.put<string>("string_val",sval);
                bval=true;
                mdplain.put<bool>("bool_val",bval);
                cout << "Succeeded - trying matching get methods"<<endl;
                cout << "long_val="<<mdplain.get<long>("long_val")<<endl;
                cout << "double_val="<<mdplain.get<double>("double_val")<<endl;
                cout << "string_val="<<mdplain.get<string>("string_val")<<endl;
                cout << "bool_val="<<mdplain.get<bool>("bool_val")<<endl;
                cout << "Same thing using operator >> "<<endl;
		cout << mdplain;
		cout << "Trying simple file read constructor"<<endl
                    << "Reading from simple.txt"<<endl;
                ifstream ifs("simple.txt");
                Metadata mds(ifs);
		cout << mds;
                cout << "Trying to read more complex pf file using AntelopePF object constructor"<<endl;
                AntelopePf pfsmd(pfname);
                cout << "Success - read the following:  "<<endl
                    << pfsmd<<endl;
                cout << "Trying assignment operator for Metadata with RTTI"<<endl;
                Metadata mdsum;
                mdsum=dynamic_cast<Metadata&>(pfsmd);
                cout << "Worked"<<endl<<"Contents of copy (simple attributes ony)"<<endl;
                cout << mdsum<<endl;
                cout << "Trying += operator.  Merging inline and pf objects"<<endl;
                cout << "Trying to add simple to Metadata derived from pf"<<endl;
                mdsum+=mds;
                cout << "Done - result:"<<endl;
                cout << mdsum<<endl;
                cout << "Reading and writing a couple of simple parameters"<<endl;
                cout << "simple_real_parameter="
                    <<pfsmd.get<double>("simple_real_parameter")<<endl
                  << "simple_int_parameter="
                    <<pfsmd.get<int>("simple_int_parameter")<<endl
                  << "simple_bool_parameter="<<pfsmd.get_bool("simple_bool_parameter")
                  <<endl;
                cout << "Trying get_tbl method"<<endl;
                list<string> tsttbl;
                tsttbl=pfsmd.get_tbl("mdlist");
                cout << "mdlist Tbl extracted from pf"<<endl;
                list<string>::iterator iptr;
                for(iptr=tsttbl.begin();iptr!=tsttbl.end();++iptr)
                {
                  cout << *iptr<<endl;
                }
                cout << "Trying get_branch method - extracting test_nested_tag"
                  <<endl;
                AntelopePf pfbr(pfsmd.get_branch("test_nested_tag"));
                cout << "Success"<<endl
                    <<"Contents"<<endl
                    << dynamic_cast<Metadata&>(pfbr)<<endl;
                cout << "test_double parameter in branch="<<pfbr.get_double("test_double")<<endl;
                cout << "Testing exceptions.  First a get failure:"<<endl;
                try{
                    double dbad=mdsum.get<double>("bad_key");
                }catch(MetadataGetError& mdge)
                {
                    cout << "Properly handled.  Message posted follows:"<<endl
                        << mdge.what()<<endl;
                }
                cout << "Trying intentional type mismatch."<<endl;
                try{
                    int ibad;
                    ibad=pfbr.get<int>("test_double");
                }catch(MetadataGetError& mdge)
                {
                    cout << "Properly handled trying to get test_double as int"
                        <<endl
                        <<"Error message posted"<<endl
                        << mdge.what()<<endl;
                }

	}
	catch (MsPASSError& sess)
	{
            cout << "Something threw an MsPASSError exception - message posted follows"<<endl;
	    cout << sess.what()<<endl;
	}
        catch(std::exception& stex)
        {
            cout << "Something threw a std::exception that was not a MsPASSError"<<endl
                << "Error message:  "<<stex.what()<<endl;
	
        }
}
