import simpy
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from datetime import datetime

# Cargar configuración
with open('config.json') as f:
    config = json.load(f)

# Configuración inicial
random.seed(10)  # Semilla para reproducibilidad
TIEMPO_SIMULACION = config['tiempo_simulacion']
NUM_ENFERMERAS = config['recursos']['enfermeras']
NUM_DOCTORES = config['recursos']['doctores']
NUM_RAYOS_X = config['recursos']['rayos_x']

# Datos para análisis
tiempos_espera = []
tiempos_triage = []
tiempos_doctor = []
tiempos_rayos = []
pacientes_atendidos = 0
pacientes = []  # Lista para almacenar todos los pacientes

class Paciente:
    def __init__(self, id):
        self.id = id
        self.severidad = random.randint(1, 5)  # 1=urgente, 5=no urgente
        self.tiempo_llegada = 0
        self.tiempo_atencion = 0
        self.tiempo_triage = 0
        self.tiempo_doctor = 0
        self.tiempo_rayos = 0

def llegada_pacientes(env, enfermeras, doctores, rayos_x):
    global pacientes_atendidos
    paciente_id = 0
    while True:
        # Llegada exponencial según configuración
        yield env.timeout(random.expovariate(1/config['tiempos']['llegada_media']))
        paciente_id += 1
        paciente = Paciente(paciente_id)
        paciente.tiempo_llegada = env.now
        pacientes.append(paciente)  # Agregar a la lista de pacientes
        env.process(flujo_paciente(env, paciente, enfermeras, doctores, rayos_x))

def flujo_paciente(env, paciente, enfermeras, doctores, rayos_x):
    global pacientes_atendidos, tiempos_espera, tiempos_triage, tiempos_doctor, tiempos_rayos
    
    # Paso 1: Triage con enfermera
    with enfermeras.request(priority=paciente.severidad) as req:
        yield req
        inicio_triage = env.now
        yield env.timeout(random.uniform(
            config['tiempos']['triage_min'],
            config['tiempos']['triage_max']
        ))
        fin_triage = env.now
        paciente.tiempo_triage = fin_triage - inicio_triage
        tiempos_triage.append(paciente.tiempo_triage)
        print(f"[{env.now:.1f}] Paciente {paciente.id} completó triage (Severidad {paciente.severidad})")
    
    # Paso 2: Atención médica
    with doctores.request(priority=paciente.severidad) as req:
        yield req
        inicio_doctor = env.now
        yield env.timeout(random.uniform(
            config['tiempos']['doctor_min'],
            config['tiempos']['doctor_max']
        ))
        fin_doctor = env.now
        paciente.tiempo_doctor = fin_doctor - inicio_doctor
        tiempos_doctor.append(paciente.tiempo_doctor)
        print(f"[{env.now:.1f}] Paciente {paciente.id} atendido por doctor")
    
    # Paso 3: Exámenes según probabilidad configurada
    if random.random() < config['probabilidades']['necesita_rayos']:
        with rayos_x.request(priority=paciente.severidad) as req:
            yield req
            inicio_rayos = env.now
            yield env.timeout(random.uniform(
                config['tiempos']['rayos_min'],
                config['tiempos']['rayos_max']
            ))
            fin_rayos = env.now
            paciente.tiempo_rayos = fin_rayos - inicio_rayos
            tiempos_rayos.append(paciente.tiempo_rayos)
            print(f"[{env.now:.1f}] Paciente {paciente.id} completó rayos X")
    
    # Registro de datos
    paciente.tiempo_atencion = env.now - paciente.tiempo_llegada
    tiempos_espera.append(paciente.tiempo_atencion)
    pacientes_atendidos += 1

def analizar_colas():
    # Crear DataFrame solo con los pacientes que han sido atendidos
    df = pd.DataFrame({
        'tiempo_espera': tiempos_espera,
        'severidad': [p.severidad for p in pacientes[:len(tiempos_espera)]],
        'tiempo_triage': [p.tiempo_triage for p in pacientes[:len(tiempos_espera)]],
        'tiempo_doctor': [p.tiempo_doctor for p in pacientes[:len(tiempos_espera)]],
        'tiempo_rayos': [p.tiempo_rayos for p in pacientes[:len(tiempos_espera)]]
    })
    
    print("\n=== Análisis por Severidad ===")
    print(df.groupby('severidad').describe())
    
    print("\n=== Tiempos Promedio ===")
    print(f"Triage: {np.mean(tiempos_triage):.2f} minutos")
    print(f"Doctor: {np.mean(tiempos_doctor):.2f} minutos")
    print(f"Rayos X: {np.mean(tiempos_rayos):.2f} minutos")
    print(f"Total: {np.mean(tiempos_espera):.2f} minutos")

def generar_graficas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gráfico de tiempos de espera
    plt.figure(figsize=(10, 6))
    plt.hist(tiempos_espera, bins=15, color='skyblue', edgecolor='black')
    plt.title("Distribución del Tiempo Total de Atención")
    plt.xlabel("Minutos")
    plt.ylabel("Número de Pacientes")
    plt.savefig(f"tiempos_atencion_{timestamp}.png")
    plt.close()
    
    # Gráfico de uso de recursos
    recursos = ['Enfermeras', 'Doctores', 'Rayos X']
    cantidades = [NUM_ENFERMERAS, NUM_DOCTORES, NUM_RAYOS_X]
    plt.figure(figsize=(8, 5))
    plt.bar(recursos, cantidades, color=['#4CAF50', '#2196F3', '#FF9800'])
    plt.title("Configuración de Recursos")
    plt.ylabel("Cantidad")
    plt.savefig(f"configuracion_recursos_{timestamp}.png")
    plt.close()
    
    # Gráfico de tiempos por severidad
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame({
        'severidad': [p.severidad for p in pacientes],
        'tiempo_total': [p.tiempo_atencion for p in pacientes]
    })
    df.boxplot(column='tiempo_total', by='severidad')
    plt.title("Tiempos de Atención por Severidad")
    plt.xlabel("Severidad")
    plt.ylabel("Minutos")
    plt.savefig(f"tiempos_severidad_{timestamp}.png")
    plt.close()

def main():
    env = simpy.Environment()
    enfermeras = simpy.PriorityResource(env, capacity=NUM_ENFERMERAS)
    doctores = simpy.PriorityResource(env, capacity=NUM_DOCTORES)
    rayos_x = simpy.PriorityResource(env, capacity=NUM_RAYOS_X)
    
    env.process(llegada_pacientes(env, enfermeras, doctores, rayos_x))
    env.run(until=TIEMPO_SIMULACION)
    
    # Resultados
    print("\n=== Resultados ===")
    print(f"Pacientes atendidos: {pacientes_atendidos}")
    analizar_colas()
    generar_graficas()

if __name__ == "__main__":
    main()