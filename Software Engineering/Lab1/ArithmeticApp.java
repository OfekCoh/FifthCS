import java.util.ArrayList; //for the calculations array
import java.util.Stack; //to help organize operators
import java.util.Scanner; //to receive data from user

public class ArithmeticApp {
    private static boolean divide_by_zero = false;//tells the user if number was divided by zero

    public static void main(String[] args)
    {
        boolean validBase = false;
        int base = 0;
        int final_result;
        String[] input_array;
        ArrayList<String> calculation_array;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter base (2/8/10/16):"); // Prompt user
        while(!validBase){
            try {
                base = scanner.nextInt(); // Try reading an integer
                validBase = base == 2 || base == 8 || base == 10 || base == 16; //validate the base
                if(!validBase){
                    System.out.println("Error – this base isn’t supported. Please enter a base (2/8/10/16):");
                }
            } catch (Exception e) {
                System.out.println("Error – this base isn’t supported. Please enter a base (2/8/10/16):"); //handle non-integer inputs
                scanner.next(); //clear the invalid input

            }
        }
        scanner.nextLine();//consume the leftover newline from nextInt()

        System.out.println("Enter expression: ");//receive expression
        String input = scanner.nextLine();
        scanner.close();//close the scanner
        if(input.isEmpty()){//the expression is empty
            System.out.println("Error: invalid expression");
        }
        else {
            input_array = prepareArr(input, base);
            if(input_array == null) {
                System.out.println("Error: invalid expression");
            }
            else{

                calculation_array = calculation_array(input_array);
                final_result = result(calculation_array, base);
                if(!divide_by_zero){
                    System.out.println("The value of expression " + input + " is : " + convertResult(final_result, base).toUpperCase());
                }
                else {
                    System.out.println("Error: trying to divide by 0 (evaluated: \"0\")");
                }
            }
        }

    }

    //use calculation string to calculate the result
    public static int result(ArrayList<String> calculation_array, int base){
        Stack<Integer> stack = new Stack<>();
        int a;
        int b;

        //iterate through calculations array to calculate the result
        for (String element : calculation_array) {
            if (isOperator(element)) { //when reaches operator, calculate using the top 2 numbers in the stack and push the result
                if(!element.equals("~")){
                    b = stack.pop();
                    a = stack.pop();
                    if(element.equals("/") && b == 0){//check divide by zero
                        divide_by_zero = true;
                        return 0;
                    }
                    stack.push(applyOperator(a, b, element));
                }
                else{
                    a = stack.pop();
                    stack.push(~a);
                }
            }
            else {
                stack.push(Integer.parseInt(element, base)); //insert base 10 numbers to the stack
            }
        }
        return stack.pop(); //the result will be what's left in the stack
    }

    //calculate result between 2 numbers and operator
    public static int applyOperator(int a, int b, String operator) {
        switch (operator) {
            case "+": return a + b;
            case "-": return a - b;
            case "*": return a * b;
            case "/": return a / b;
            case "^": return a ^ b;
            case "&": return a & b;
            case "|": return a | b;
            case "~": return  ~a;
            default: return 0;
        }
    }

    //remove spaces, handle unary -, create array of operators and numbers, check validity
    public static String[] prepareArr(String input, int base){
        //check spcaces
        if(hasSpaceBetweenNumbers(input, base)){
            return null;
        }
        //remomve spaces
        input = input.replace(" ","");
        if(!isValid(input, base)){
            return null;
        }
        //handle -(-
        input = input.replace("-(-","+(");
        input = input.replace("(+","(");
        if(input.charAt(0) == '+'){
            input = input.substring(1);
        }
        //handle unary -
        input = input.replace("(-","(0-");
        if(input.charAt(0) == '-'){
            input = "00000000"+input;
        }
        //tokenize string and check validity
        String[] input_array = input.split("(?=[()+\\-*/&^|~])|(?<=[()+\\-*/&^|~])");
        if(base == 2){
            //check if the base is 2 if the numbers are 8bit
            for(String element : input_array){
                if(!isOperator(element)){
                    if(element.length() != 8){
                        return null;
                    }
                }
            }

        }
        return input_array;
    }

    //check for spaces inside numbers
    public static boolean hasSpaceBetweenNumbers(String input, int base) {
        // Regular expression for numbers based on the base
        String regex = "";

        switch (base) {
            case 10:  // Decimal numbers
                regex = "\\d+";  // Matches one or more digits
                break;
            case 8:
                regex = "[0-7]+";  // Matches numbers starting with '0x' and followed by hex digits
                break;
            case 16:  // Hexadecimal numbers
                regex = "[0-9A-F]+";  // Matches numbers starting with '0x' and followed by hex digits
                break;
            case 2:  // Binary numbers
                regex = "[01]+";  // Matches numbers starting with '0b' and followed by binary digits
                break;
            default:
                return false;  // Return false if unsupported base
        }

        // Modify the regex to find two numbers with spaces between them
        String fullRegex = regex + "\\s+" + regex;

        // Check if the string matches the pattern (two valid numbers with spaces)
        return input.matches(".*" + fullRegex + ".*");

    }

    //check input validity and change the input string to a string builder used to calculate output in order
    public static ArrayList<String> calculation_array(String[] input_array) {
        ArrayList<String> calculation_array = new ArrayList<>(); //more efficient method to append writing elements in loo
        Stack<String> operators = new Stack<>(); //stack to help organize operators by precedence

        //iterate through the input array and build the calculation array
        for( String element : input_array){
            if (isOperator(element)) {// if the current element is operator

                if (element.equals("(")) { //open parentheses
                    operators.push(element);
                }

                //close parentheses, removing operators until ( will make sure that whats inside the parentheses hava higher priority
                else if (element.equals(")")) {
                    while (!operators.isEmpty() && !operators.peek().equals("(")) {
                        calculation_array.add(operators.pop());
                    }
                    if (!operators.isEmpty()) {
                        operators.pop(); //pop '('
                    }
                }

                else{

                    //make sure that higher priority operators will come first
                    while (!operators.isEmpty() && precedence(operators.peek()) >= precedence(element)) {
                        calculation_array.add(operators.pop());
                    }
                    operators.push(element);
                }
            }
            else{//the elements is a number or empty
                if (!element.equals(" ")) {//insert the elemenet if not space
                    calculation_array.add(element);
                }

            }
        }

        //add remaining operators
        while(!operators.isEmpty()) {
            calculation_array.add(operators.pop());
        }
        return calculation_array; // return calculations array
    }

    //returns the operators precedence to help determine which operators will be calculated first
    public static int precedence(String operator) {
        switch (operator) {
            case "+":
            case "-":
            case "|":
                return 1; //lowest precedence
            case "*":
            case "/":
            case "^":
                return 2; //highest precedence
            case "&":
                return 3;
            case "~":
                return 4;

            default:
                return 0;
        }
    }

    //check if element is operator
    private static boolean isOperator(String element) {
        return "+-*/)(&^|~".contains(element);
    }

    //check input validity
    public static boolean isValid(String input, int base) {
        char prevChar;
        String validChars = "0123456789ABCDEF";//the possible values for a number
        validChars = validChars.substring(0, base);
        Stack<Character> parentheses = new Stack<>();//to check if all ()
        boolean two_operators;//check case of 2 operators in a row
        String operators;
        boolean binary_operators = isBinaryExpression(input);
        //legal operators for base
        if(base == 2 && binary_operators) {
            operators = "|&~^)(";//binary operators
        }else{
            operators = "+-*/)(";
        }
        prevChar = input.charAt(0);
        if( (!operators.contains(Character.toString(prevChar)) && !validChars.contains(Character.toString(prevChar)))) {
            return false; //invalid character
        }
        if(base == 2 && binary_operators){
            if((operators.contains(Character.toString(prevChar)) && prevChar != '~' && prevChar != '(')){//expression start in operator
                return false;//first member is operator other than 0 or not a valid character
            }
        }else{
            if(operators.contains(Character.toString(prevChar)) && prevChar != '-' && prevChar != '('){//expression start in operator
                return false;//first member is operator other than 0 or not a valid character
            }
        }
        if(prevChar == '('){//to make sure () is valid
            parentheses.push(prevChar);
        }

        //iterate through the string starting from the second member
        for(char ch : input.substring(1).toCharArray()){
            if(!operators.contains(Character.toString(ch)) && !validChars.contains(Character.toString(ch))){
                return false;//invalid character
            }
            if(base == 2 && binary_operators){
                two_operators =  !(prevChar == ')' && ch == '~') &&  !(prevChar == '~' && ch == '~') && (ch == '(' || ch == '~' || prevChar == ')');//legal situation for 2 operators in a row
            }
            else {
                two_operators = (prevChar == '(' && ch == '-') || prevChar == ')' || ch == '(';//legal situation for 2 operators in a row
            }

            if(operators.contains(Character.toString(prevChar)) && operators.contains(Character.toString(ch)) && !two_operators){
                return false;//2 operators in a row, no - or ()
            }
            if (!operators.contains(Character.toString(prevChar)) && ch =='(') {
                return false;//the case number(
            }
            if (validChars.contains(Character.toString(ch)) && prevChar ==')') {
                return false;//the case )number
            }
            if (validChars.contains(Character.toString(prevChar)) && ch =='~') {
                return false;//the case number~
            }
            if(ch == '(' && prevChar == ')'){
                return false;//)( case
            }

            if (ch == '(') {
                parentheses.push(ch);
            } else if (ch == ')') {
                if (parentheses.isEmpty() || parentheses.pop() != '(') return false;// close ) without open
            }

            prevChar = ch;
        }
        if(operators.contains(Character.toString(input.charAt(input.length()-1))) && input.charAt(input.length()-1) != ')'){
            return false;//end in, operator not )
        }
        return parentheses.isEmpty();//return true if didn't find invalid chars and parentheses are balanced
    }

    //check if arithmetic or binary expression
    public static boolean isBinaryExpression(String input) {
        String arithmetics = "+-*/";
        String binaries = "~&|";
        for(char ch : input.toCharArray()){
            if(arithmetics.contains(Character.toString(ch))){
                return false;
            }
            if(binaries.contains(Character.toString(ch))){
                return true;
            }
        }
        return true;
    }

    //convert the 10 base result back to its base
    public static String convertResult(int result, int base){
        switch (base) {
            case 10:
                return Integer.toString(result);  // Return result as string for base 10
            case 8:
                if (result < 0) {
                    return "-" + Integer.toOctalString(-result);  // Negative result for octal
                } else {
                    return Integer.toOctalString(result);  // Positive result for octal
                }
            case 2:
                // Convert the integer to a binary string
                String binaryString = Integer.toBinaryString(result);

                // If the number is negative or has fewer than 8 bits, pad it with leading zeros
                if (binaryString.length() < 8) {
                    // Pad with leading zeros to ensure the string is 8 bits long
                    binaryString = String.format("%8s", binaryString).replace(' ', '0');
                } else if (binaryString.length() > 8) {
                    // Ensure the result is exactly 8 bits (this handles cases when the number exceeds 8 bits)
                    binaryString = binaryString.substring(binaryString.length() - 8);
                }

                return binaryString;
            case 16:
                if (result < 0) {
                    return "-" + Integer.toHexString(-result);  // Negative result for hexadecimal
                } else {
                    return Integer.toHexString(result);  // Positive result for hexadecimal
                }
            default:
                return " ";  // Return a space if the base is unsupported
        }
    }



}
