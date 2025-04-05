package com.example;

public class Main {
    public static void main(String[] args) {
        VectorHeap<Integer> heap = new VectorHeap<>();
        
        // Agregar elementos
        heap.add(5);
        heap.add(3);
        heap.add(7);
        heap.add(1);
        heap.add(9);
        
        // Remover elementos (deberían salir en orden ascendente)
        System.out.println("Elementos removidos del heap:");
        while (!heap.isEmpty()) {
            System.out.println(heap.remove());
        }
    }
}