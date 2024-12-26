import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Method;


@Retention(RetentionPolicy.RUNTIME) // The annotation is available at runtime
public @interface SimpleAnnotation {
    String message(); // Define an attribute
}

class A {
    @SimpleAnnotation(message = "Hello, this is a custom annotation!")
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

        Method method = a.getClass().getMethod("show");
        if (method.isAnnotationPresent(SimpleAnnotation.class)) {
            SimpleAnnotation annotation = method.getAnnotation(SimpleAnnotation.class);
            System.out.println("Annotation message: " + annotation.message());
        }
    }
}