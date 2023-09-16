import tensorflow as tf
from math import floor
from pymongo import MongoClient


class LoginAnomalyDetector:
    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs=100)

    def predict(self, X_test):
        y_pred = self.model.predict(X_test)
        return y_pred

    def detect_anomalies(self, X_test, threshold=0.5):
        y_pred = self.predict(X_test)
        anomaly_scores = y_pred[:, 0]

        anomalies = []
        for i in range(len(anomaly_scores)):
            if anomaly_scores[i] > threshold:
                anomalies.append(i)

        return anomalies


def main():
    conn = MongoClient()               
    db = conn.Logs  
    securityLogs = db.SecurityLogs 
    cursor = securityLogs.find({"EventMessage", "EventType", "EventTime", "event_ids": {"$in": [14, 15]}})
    data = []
    for x in cursor:
        data.append(x)
    X_train_filtered, y_train_filtered = data[:floor(len(data)*0.8)], data[:(1-floor(len(data)*0.8))]
    conn.close()
    cursor.close()
    anomaly_detector = LoginAnomalyDetector()
    anomaly_detector.train(X_train_filtered, y_train_filtered)

    anomalies = anomaly_detector.detect_anomalies(X_train_filtered)

    print('Detected anomalies:')
    for anomaly in anomalies:
        print(anomaly)

if __name__ == '__main__':
    
    
    main()