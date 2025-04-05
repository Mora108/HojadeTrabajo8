package com.example;

import java.util.ArrayList;
import java.util.List;

public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    private final List<E> heap = new ArrayList<>();

    // Métodos auxiliares
    private int parent(int i) { return (i - 1) / 2; }
    private int left(int i) { return 2 * i + 1; }
    private int right(int i) { return 2 * i + 2; }

    @Override
    public void add(E element) {
        heap.add(element);
        percolateUp(heap.size() - 1);
    }

    private void percolateUp(int index) {
        E elemento = heap.get(index);
        while (index > 0 && elemento.compareTo(heap.get(parent(index))) < 0) {
            heap.set(index, heap.get(parent(index)));
            index = parent(index);
        }
        heap.set(index, elemento);
    }

    @Override
    public E remove() {
        if (isEmpty()) throw new IllegalStateException("Heap vacío");
        E min = heap.get(0);
        E last = heap.remove(heap.size() - 1);
        if (!isEmpty()) {
            heap.set(0, last);
            percolateDown(0);
        }
        return min;
    }

    private void percolateDown(int index) {
        int smallest = index;
        int left = left(index);
        int right = right(index);

        if (left < heap.size() && heap.get(left).compareTo(heap.get(smallest)) < 0) {
            smallest = left;
        }
        if (right < heap.size() && heap.get(right).compareTo(heap.get(smallest)) < 0) {
            smallest = right;
        }
        if (smallest != index) {
            swap(index, smallest);
            percolateDown(smallest);
        }
    }

    private void swap(int i, int j) {
        E temp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, temp);
    }

    @Override
    public boolean isEmpty() { return heap.isEmpty(); }

    @Override
    public int size() { return heap.size(); }
}