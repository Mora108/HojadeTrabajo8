package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PacienteTest {
    
    @Test
    public void testConstructorYGetters() {
        Paciente p = new Paciente("Juan", "Dolor", 'A');
        assertEquals("Juan", p.getNombre());
        assertEquals("Dolor", p.getSintoma());
        assertEquals('A', p.getCodigo());
    }

    @Test
    public void testCompareTo() {
        Paciente p1 = new Paciente("Juan", "Dolor", 'A');  // Prioridad más alta
        Paciente p2 = new Paciente("Maria", "Fiebre", 'B'); // Prioridad media
        Paciente p3 = new Paciente("Pedro", "Tos", 'C');    // Prioridad baja
        
        assertTrue(p1.compareTo(p2) < 0, "A debe tener mayor prioridad que B");
        assertTrue(p2.compareTo(p3) < 0, "B debe tener mayor prioridad que C");
        assertTrue(p1.compareTo(p3) < 0, "A debe tener mayor prioridad que C");
        assertEquals(0, p1.compareTo(new Paciente("Ana", "Gripe", 'A')), "Misma prioridad debe retornar 0");
    }
} 