
import java.io*;
import java.lang.*;
 class program1
{
public Static void main(String args[])throws IOException
{
System.out.println("Extract the portion of the string and print the extracted string");
BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
String input_string=br.readLine();
System.out.print("Enter the start index");
int start=Integer.parsent(br.readLine());
System.out.println("Enter the end index");
int end=Integer.paseInt(br.readLine());
String output_string=input_string.substring(start,end);
Sysetm.out.print("Extracted string is " +output_string);
}
}
 