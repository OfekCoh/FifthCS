

class A {
    public void show(){
        System.out.println("A");
    }
}

// @Deprecated
class B extends A {
    @Override
    public void show(){
        System.out.println("B");
    }
}

public class Main {
    public static void main(String[] args) {
        A a = new A();
        B b = new B();

        a.show(); // Prints "A"
        b.show(); // Prints "B"
    }
}