package com.example;

public class Paciente implements Comparable<Paciente> {
    private final String nombre;
    private final String sintoma;
    private final char codigoEmergencia;

    public Paciente(String nombre, String sintoma, char codigo) {
        this.nombre = nombre;
        this.sintoma = sintoma;
        this.codigoEmergencia = codigo;
    }

    private int getPrioridad() {
        return codigoEmergencia - 'A' + 1; // A=1, B=2, ..., E=5
    }

    @Override
    public int compareTo(Paciente otro) {
        return Integer.compare(this.getPrioridad(), otro.getPrioridad());
    }

    // Getters
    public String getNombre() { return nombre; }
    public String getSintoma() { return sintoma; }
    public char getCodigo() { return codigoEmergencia; }
}