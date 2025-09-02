'use client';

import { useState, useRef, useEffect } from 'react';
import { BrowserMultiFormatReader, NotFoundException } from '@zxing/browser';
import styles from './BarcodeScanner.module.css';

export default function BarcodeScanner({ onScan }: { onScan: (result: string) => void }) {
  const [isScanning, setIsScanning] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const codeReader = new BrowserMultiFormatReader();

  useEffect(() => {
    if (isScanning) {
      codeReader.decodeFromVideoDevice(undefined, videoRef.current, (result, err) => {
        if (result) {
          onScan(result.getText());
          setIsScanning(false);
        }
        if (err && !(err instanceof NotFoundException)) {
          console.error(err);
        }
      });
    }
    return () => {
      codeReader.reset();
    };
  }, [isScanning]);

  return (
    <div>
      <button type="button" onClick={() => setIsScanning(true)}>Scan Barcode</button>
      {isScanning && (
        <div className={styles.modalOverlay}>
          <div className={styles.modalContent}>
            <video ref={videoRef} className={styles.video}></video>
            <button onClick={() => setIsScanning(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
