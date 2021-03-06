<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>680</width>
    <height>534</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Multi-user Pyramid (MUP)</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 177, 145, 255), stop:1 rgba(110, 94, 114, 255))</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLineEdit" name="lineEdit">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>480</y>
      <width>321</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>MS Reference Sans Serif</family>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(236, 160, 81, 255), stop:1 rgba(174, 113, 115, 255))</string>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>340</x>
      <y>20</y>
      <width>321</width>
      <height>501</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(236, 160, 81, 255), stop:1 rgba(174, 113, 115, 255))</string>
    </property>
   </widget>
   <zorder>textEdit</zorder>
   <zorder>lineEdit</zorder>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
