package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

public class VectorHeapTest {

    @Test
    public void testAddAndRemove() {
        VectorHeap<Paciente> heap = new VectorHeap<>();
        Paciente pA = new Paciente("A", "Síntoma A", 'A');
        Paciente pB = new Paciente("B", "Síntoma B", 'B');

        heap.add(pA);
        heap.add(pB);
        assertEquals(pA, heap.remove());
        assertEquals(pB, heap.remove());
    }

    @Test
    public void testIsEmpty() {
        VectorHeap<Paciente> heap = new VectorHeap<>();
        assertTrue(heap.isEmpty());
        heap.add(new Paciente("C", "Síntoma C", 'C'));
        assertFalse(heap.isEmpty());
    }

    @Test
    public void testRemoveEmptyHeap() {
        VectorHeap<Paciente> heap = new VectorHeap<>();
        IllegalStateException exception = assertThrows(IllegalStateException.class, heap::remove);
        assertEquals("Heap vacío", exception.getMessage());
    }
}