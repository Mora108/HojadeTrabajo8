package com.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class EmergenciasVectorHeap {
    public static void main(String[] args) {
        PriorityQueue<Paciente> cola = new VectorHeap<>();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(
                    EmergenciasVectorHeap.class.getResourceAsStream("/pacientes.txt")))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] datos = line.split(", ");
                Paciente paciente = new Paciente(
                    datos[0].trim(),
                    datos[1].trim(),
                    datos[2].trim().charAt(0)
                );
                cola.add(paciente);
            }
        } catch (IOException e) {
            System.err.println("Error leyendo el archivo: " + e.getMessage());
        }

        // Atender pacientes
        while (!cola.isEmpty()) {
            Paciente p = cola.remove();
            System.out.printf("%s - %s (Prioridad %c)%n",
                p.getNombre(), p.getSintoma(), p.getCodigo());
        }
    }
}