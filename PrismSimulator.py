import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.patches as patches

class SimplePrismSimulator:
    def __init__(self):
        # Prizma malzemeleri ve kırılma indisleri - Standart optik cam
        self.materials = {
            'Optik Cam': {
                'red': 1.5145, 'orange': 1.5170, 'yellow': 1.5185,
                'green': 1.5200, 'blue': 1.5230, 'violet': 1.5270
            }
        }
        
        # Spektrum renkleri ve dalga boyları (nm)
        self.wavelengths = {
            'violet': 434, 'blue': 486, 'green': 510,
            'yellow': 546, 'orange': 589, 'red': 656
        }
        
        # Renk kodları
        self.colors = {
            'violet': '#8B00FF', 'blue': '#0066FF', 'green': '#00FF66',
            'yellow': '#FFFF00', 'orange': '#FF8000', 'red': '#FF0000'
        }
        
        # Başlangıç parametreleri
        self.prism_angle = 60
        self.incident_angle = 45
        self.material = 'Optik Cam'  # Sabit malzeme
        self.n_air = 1.000  # Havanın kırılma indisi
        
        # Tema renkleri
        self.bg_color = '#f5f5f5'
        self.panel_color = '#ffffff'
        self.accent_color = '#4285F4'
        self.text_color = '#333333'
        
        self.setup_interface()
    
    def setup_interface(self):
        """Basit ve temiz arayüz"""
        plt.rcParams['toolbar'] = 'None'
        
        # Ana pencere
        self.fig = plt.figure(figsize=(18, 10), facecolor=self.bg_color)
        self.fig.canvas.manager.set_window_title('CAL')  # Pencere başlığını değiştir
        self.fig.suptitle('Prizma Optik Simulatörü',  # Başlığı kısalt
                         fontsize=18, fontweight='bold', color=self.accent_color)
        
        # Basit grid layout - 3x3
        self.create_panels()
        self.create_sliders()
        self.update_simulation()
    
    def create_panels(self):
        """Panel'leri oluştur - basit grid"""
        # Ana prizma paneli - sol üst, büyük
        self.ax_main = plt.subplot2grid((4, 3), (0, 0), rowspan=2, colspan=1, facecolor=self.panel_color)
        self.ax_main.set_title('Prizma Analizi', fontsize=14, color=self.text_color, pad=15)
        
        # Hesaplamalar paneli - orta üst
        self.ax_calc = plt.subplot2grid((4, 3), (0, 1), facecolor=self.panel_color)
        self.ax_calc.set_title('Fizik Hesaplamaları', fontsize=12, color=self.text_color)
        
        # Sonuçlar paneli - orta alt
        self.ax_result = plt.subplot2grid((4, 3), (1, 1), facecolor=self.panel_color)
        self.ax_result.set_title('Sonuçlar', fontsize=12, color=self.text_color)
        
        # Dispersiyon paneli - sağ, büyük
        self.ax_dispersion = plt.subplot2grid((4, 3), (0, 2), rowspan=2, facecolor=self.panel_color)
        self.ax_dispersion.set_title('Dalga Boyu - Sapma Açısı Grafiği', fontsize=12, color=self.text_color)
        
        # Yeni açıklama paneli - alt orta
        self.ax_info = plt.subplot2grid((4, 3), (2, 1), facecolor=self.panel_color)
        self.ax_info.set_title('Değişken Açıklamaları', fontsize=10, color=self.text_color)
        self.ax_info.axis('off')
        
        # Sabit açıklamalar
        info_text = """n: Kırılma indisi
i₁: Giriş açısı
A: Prizma açısı
r₁: İlk kırılma açısı
i₂: İkinci giriş açısı
r₂: İkinci kırılma açısı
δ: Sapma açısı"""
        
        self.ax_info.text(0.1, 0.9, info_text, ha='left', va='top',
                         fontsize=9, family='monospace',
                         transform=self.ax_info.transAxes)
    
    def create_sliders(self):
        """Slider'lar - Prizma analizi panelinin hemen altında, alt alta, aynı hizada"""
        
        # Prizma analizi panelinin pozisyonunu al
        main_panel_pos = self.ax_main.get_position()
        
        # Slider boyutları
        slider_height = 0.03
        slider_width = main_panel_pos.width  # Ana panelin genişliği ile aynı
        slider_spacing = 0.04  # Slider'lar arası dikey boşluk
        
        # Başlangıç pozisyonu - ana panelin hemen altında
        slider_start_x = main_panel_pos.x0    # Ana panelin sol kenarı ile hizalı
        slider_start_y = main_panel_pos.y0 - 0.06   # Ana panelin hemen altında
        
        # Prizma açısı slider'ı - üstte
        ax_prism = plt.axes([slider_start_x, slider_start_y, slider_width, slider_height], 
                            facecolor='white')
        self.slider_prism_angle = Slider(
            ax_prism, 'Prizma Açısı', 30, 90,
            valinit=self.prism_angle, valfmt='%.0f°',
            color=self.accent_color, track_color='#e0e0e0'
        )
        
        # Geliş açısı slider'ı - altta  
        ax_incident = plt.axes([slider_start_x, slider_start_y - slider_spacing, 
                               slider_width, slider_height], facecolor='white')
        self.slider_incident = Slider(
            ax_incident, 'Geliş Açısı', 15, 75,
            valinit=self.incident_angle, valfmt='%.0f°',
            color=self.accent_color, track_color='#e0e0e0'
        )
        
        # Event bağlantıları
        self.slider_prism_angle.on_changed(lambda val: self.update_simulation())
        self.slider_incident.on_changed(lambda val: self.update_simulation())
    
    def calculate_prism_ray_path(self, incident_angle_deg, prism_angle_deg, n_values):
        """
        Prizma ışın yolu hesaplaması - Snell yasası ve prizma geometrisi
        
        Fiziksel temeller:
        1. Snell Yasası: n₁sin(θ₁) = n₂sin(θ₂)
        2. Prizma geometrisi: i₂ = A - r₁ 
        3. Sapma açısı: δ = i₁ + r₂ - A
        """
        results = {}
        i1 = np.radians(incident_angle_deg)  # Giriş açısını radyana çevir
        A = np.radians(prism_angle_deg)      # Prizma açısını radyana çevir
        
        for color, n_prism in n_values.items():
            try:
                # İlk yüzeyde Snell yasası: n_air * sin(i₁) = n_prism * sin(r₁)
                sin_r1 = (self.n_air * np.sin(i1)) / n_prism
                
                # Tam iç yansıma kontrolü
                if abs(sin_r1) > 1:
                    results[color] = {'total_reflection': True}
                    continue
                
                r1 = np.arcsin(sin_r1)  # İlk kırılma açısı
                
                # Prizma geometrisinden: i₂ = A - r₁
                i2 = A - r1  # İkinci yüzeye geliş açısı
                
                # İkinci yüzeyde Snell yasası: n_prism * sin(i₂) = n_air * sin(r₂)
                sin_r2 = (n_prism * np.sin(i2)) / self.n_air
                
                # Tam iç yansıma kontrolü
                if abs(sin_r2) > 1:
                    results[color] = {'total_reflection': True}
                    continue
                
                r2 = np.arcsin(sin_r2)  # Çıkış açısı
                
                # Sapma açısı hesaplaması: δ = i₁ + r₂ - A
                delta = np.degrees(i1 + r2 - A)
                
                results[color] = {
                    'total_reflection': False,
                    'r1': np.degrees(r1),    # İlk kırılma açısı (derece)
                    'i2': np.degrees(i2),    # İkinci yüzeye geliş açısı (derece)
                    'r2': np.degrees(r2),    # Çıkış açısı (derece)
                    'delta': delta,          # Sapma açısı (derece)
                    'n': n_prism            # Kırılma indisi
                }
            except Exception as e:
                # Hata durumunda tam iç yansıma kabul et
                results[color] = {'total_reflection': True}
        
        return results
    
    def draw_prism(self):
        """Prizma çiz"""
        self.ax_main.clear()
        self.ax_main.set_xlim(-200, 350)
        self.ax_main.set_ylim(-150, 150)
        self.ax_main.set_aspect('equal')
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_title('Prizma Analizi', fontsize=14, color=self.text_color, pad=15)
        
        # Prizma koordinatları hesaplama
        A_rad = np.radians(self.prism_angle)
        apex_x, apex_y = 0, 80           # Tepe noktası
        base_left_x = -80 * np.tan(A_rad/2)   # Sol alt köşe
        base_right_x = 80 * np.tan(A_rad/2)   # Sağ alt köşe
        base_y = -80                     # Taban y koordinatı
        
        # Prizma köşe noktaları
        vertices = np.array([
            [apex_x, apex_y],           # Tepe
            [base_left_x, base_y],      # Sol alt
            [base_right_x, base_y],     # Sağ alt
            [apex_x, apex_y]            # Tepe (kapalı şekil için)
        ])
        
        # Prizma çizimi
        prism_patch = patches.Polygon(
            vertices[:-1], 
            facecolor='#e3f2fd', alpha=0.7,    # Açık mavi, yarı şeffaf
            edgecolor=self.accent_color, linewidth=3
        )
        self.ax_main.add_patch(prism_patch)
        
        # Prizma açısı bilgisi göster
        info_text = f'A = {self.prism_angle}°'
        self.ax_main.text(apex_x, apex_y + 25, info_text, 
                         ha='center', va='center', fontsize=10, weight='bold',
                         bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))
        
        return vertices
    
    def draw_rays(self, results, vertices):
        """Işınları çiz - dispersiyon gösterimi"""
        if not results:
            return
        
        A_rad = np.radians(self.prism_angle)
        base_left_x = vertices[1, 0]
        base_right_x = vertices[2, 0]
        base_y = vertices[1, 1]
        apex_y = vertices[0, 1]
        
        # Giriş noktası (sol yüzeyin ortası)
        entry_x = base_left_x
        entry_y = (base_y + apex_y) / 2
        
        # Gelen ışın çizimi (beyaz)
        incident_length = 120
        incident_angle_rad = np.radians(self.incident_angle)
        start_x = entry_x - incident_length * np.sin(incident_angle_rad + A_rad/2)
        start_y = entry_y - incident_length * np.cos(incident_angle_rad + A_rad/2)
        
        self.ax_main.arrow(start_x, start_y, entry_x - start_x, entry_y - start_y,
                          head_width=8, head_length=12, fc='white', ec='black',
                          linewidth=4, alpha=0.9)
        
        # Dispersiyon ışınları çizimi
        valid_results = {k: v for k, v in results.items() 
                        if not v.get('total_reflection', False)}
        
        if valid_results:
            for i, (color, result) in enumerate(valid_results.items()):
                color_code = self.colors[color]
                offset = (i - 2.5) * 2  # Renkleri ayırmak için offset
                
                # Prizma içi ışın yolu
                entry_x_offset = entry_x + offset * 0.3
                entry_y_offset = entry_y + offset * 0.5
                exit_x = base_right_x - offset * 0.3
                exit_y = entry_y + offset * 0.5
                
                # Prizma içi çizgi
                self.ax_main.plot([entry_x_offset, exit_x], [entry_y_offset, exit_y], 
                                 color=color_code, linewidth=3, alpha=0.8)
                
                # Çıkan ışın
                exit_length = 150
                exit_angle_rad = np.radians(result['r2'])
                end_x = exit_x + exit_length * np.sin(exit_angle_rad + A_rad/2)
                end_y = exit_y + exit_length * np.cos(exit_angle_rad + A_rad/2)
                
                # Çıkış ışını ok ile
                self.ax_main.arrow(exit_x, exit_y, end_x - exit_x, end_y - exit_y,
                                  head_width=6, head_length=10, fc=color_code, ec=color_code,
                                  linewidth=3, alpha=0.8)
    
    def display_calculations(self, results):
        """Hesaplamaları göster - sarı ışık referans alınır"""
        self.ax_calc.clear()
        self.ax_calc.axis('off')
        
        if 'yellow' in results and not results['yellow'].get('total_reflection'):
            result = results['yellow']
            calc_text = f"""HESAPLAMA (λ=546nm)
n = {result['n']:.4f}
i₁ = {self.incident_angle}°
A = {self.prism_angle}°

r₁ = {result['r1']:.1f}°
i₂ = {result['i2']:.1f}°
r₂ = {result['r2']:.1f}°
δ = {result['delta']:.1f}°"""
        else:
            calc_text = "TAM İÇ YANSIMA\nHesaplama yapılamadı"
        
        self.ax_calc.text(0.1, 0.9, calc_text, ha='left', va='top',
                         fontsize=10, family='monospace',
                         transform=self.ax_calc.transAxes)
    
    def display_results(self, results):
        """Sonuçları göster - tüm renklerin sapma açıları"""
        self.ax_result.clear()
        self.ax_result.axis('off')
        
        valid_results = {k: v for k, v in results.items() 
                        if not v.get('total_reflection', False)}
        
        if valid_results:
            result_text = "SAPMA AÇILARI\n" + "="*15 + "\n"
            
            # Türkçe renk isimleri
            color_names_tr = {
                'red': 'KIRMIZI',
                'orange': 'TURUNCU', 
                'yellow': 'SARI',
                'green': 'YEŞİL',
                'blue': 'MAVİ',
                'violet': 'MOR'
            }
            
            # Sapma açılarını listele
            for color, result in valid_results.items():
                tr_name = color_names_tr.get(color, color.upper())
                result_text += f"{tr_name:8}: {result['delta']:5.1f}°\n"
            
            # Dispersiyon hesaplama (max - min sapma açısı)
            deltas = [r['delta'] for r in valid_results.values()]
            dispersion = max(deltas) - min(deltas)
            result_text += f"\nDİSPERSİYON: {dispersion:.1f}°"
        else:
            result_text = "TAM İÇ YANSIMA\nIşın çıkamıyor!"
        
        self.ax_result.text(0.1, 0.9, result_text, ha='left', va='top',
                           fontsize=10, family='monospace',
                           transform=self.ax_result.transAxes)
    
    def plot_dispersion(self, results):
        """Dispersiyon grafiği - dalga boyu vs sapma açısı"""
        self.ax_dispersion.clear()
        
        valid_results = {k: v for k, v in results.items() 
                        if not v.get('total_reflection', False)}
        
        if not valid_results:
            self.ax_dispersion.text(0.5, 0.5, 'Tam İç Yansıma\nGrafik çizilemedi',
                                   ha='center', va='center', transform=self.ax_dispersion.transAxes)
            return
        
        # Veri hazırlama - dalga boyuna göre sıralı
        colors_ordered = ['violet', 'blue', 'green', 'yellow', 'orange', 'red']
        x_values, y_values, colors_list = [], [], []
        
        for color in colors_ordered:
            if color in valid_results:
                x_val = self.wavelengths[color]          # Dalga boyu (nm)
                y_val = valid_results[color]['delta']    # Sapma açısı (derece)
                
                x_values.append(x_val)
                y_values.append(y_val)
                colors_list.append(self.colors[color])
        
        if x_values:
            # Nokta grafiği (scatter plot)
            self.ax_dispersion.scatter(x_values, y_values, c=colors_list, 
                                     s=100, alpha=0.8, edgecolors='black')
            
            # Y ekseni limitlerini otomatik ayarla
            y_min, y_max = min(y_values), max(y_values)
            y_range = y_max - y_min
            if y_range > 0:
                self.ax_dispersion.set_ylim(y_min - y_range*0.1, y_max + y_range*0.1)
            
            # Değer etiketleri
            for i, (x, y) in enumerate(zip(x_values, y_values)):
                self.ax_dispersion.annotate(f'{y:.1f}°', (x, y), 
                                          xytext=(5, 5), textcoords='offset points',
                                          fontsize=8, alpha=0.7)
            
            # Bağlantı çizgisi
            self.ax_dispersion.plot(x_values, y_values, 
                                   color=self.accent_color, alpha=0.6, linewidth=2)
            
            # Eksen etiketleri
            self.ax_dispersion.set_xlabel('Dalga Boyu (nm)')
            self.ax_dispersion.set_ylabel('Sapma Açısı (°)')
            self.ax_dispersion.grid(True, alpha=0.3)
    
    def update_simulation(self):
        """Simülasyonu güncelle - tüm hesaplamaları yeniden yap"""
        # Slider değerlerini al
        self.prism_angle = self.slider_prism_angle.val
        self.incident_angle = self.slider_incident.val
        
        # Optik cam değerleri ile hesapla
        n_values = self.materials['Optik Cam']
        results = self.calculate_prism_ray_path(
            self.incident_angle, self.prism_angle, n_values
        )
        
        # Görsel elemanları güncelle
        vertices = self.draw_prism()
        self.draw_rays(results, vertices)
        self.display_calculations(results)
        self.display_results(results)
        self.plot_dispersion(results)
        
        # Ekranı güncelle
        self.fig.canvas.draw_idle()
    
    def show(self):
        """Simulatörü göster"""
        plt.tight_layout()
        plt.show()

# Program başlatma
if __name__ == "__main__":
    print("Prizma Optik Simulatoru başlatılıyor...")
    sim = SimplePrismSimulator()
    sim.show()