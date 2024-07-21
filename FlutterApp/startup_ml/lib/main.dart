import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;



void main() {
  runApp(MyApp());
}


class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Startup Business Profit Prediction',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PredictionForm(),
    );
  }
}


class PredictionForm extends StatefulWidget {
  @override
  _PredictionFormState createState() => _PredictionFormState();
}


class _PredictionFormState extends State<PredictionForm> {
  final _formKey = GlobalKey<FormState>();


  double? researchAndDevelopment;
  double? administration;
  double? marketingSpend;
  String? state;
  String? result;


  Future<Map<String, dynamic>> predict(
      double researchAndDevelopment,
      double administration,
      double marketingSpend,
      String state) async {
    final response = await http.post(
      Uri.parse('https://maths-for-ml-summative.onrender.com/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'Research_And_Development': researchAndDevelopment,
        'Administration': administration,
        'Marketing_Spend': marketingSpend,
        'State': state,
      }),
    );


    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load prediction');
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Startup Business Profit Prediction'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Research and Development'),
                keyboardType: TextInputType.number,
                onSaved: (value) => researchAndDevelopment = double.tryParse(value!),
                validator: (value) => value!.isEmpty ? 'Please enter a value' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Administration'),
                keyboardType: TextInputType.number,
                onSaved: (value) => administration = double.tryParse(value!),
                validator: (value) => value!.isEmpty ? 'Please enter a value' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Marketing Spend'),
                keyboardType: TextInputType.number,
                onSaved: (value) => marketingSpend = double.tryParse(value!),
                validator: (value) => value!.isEmpty ? 'Please enter a value' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'State'),
                onSaved: (value) => state = value,
                validator: (value) => value!.isEmpty ? 'Please enter a state' : null,
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  if (_formKey.currentState!.validate()) {
                    _formKey.currentState!.save();


                    try {
                      final prediction = await predict(
                        researchAndDevelopment!,
                        administration!,
                        marketingSpend!,
                        state!,
                      );


                      setState(() {
                        result = 'Business Profit: ${prediction['business profit']}';
                      });
                    } catch (e) {
                      setState(() {
                        result = 'Error: $e';
                      });
                    }
                  }
                },
                child: Text('Predict'),
              ),
              if (result != null) ...[
                SizedBox(height: 20),
                Text(result!),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

