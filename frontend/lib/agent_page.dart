import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'dart:convert';
import 'dart:math';

class AgentPage extends StatefulWidget {
  const AgentPage({super.key});

  @override
  State<AgentPage> createState() => _AgentPageState();
}

class _AgentPageState extends State<AgentPage> {
  final List<Map<String, String>> _messages = [];
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _voiceInput = '';
  String _sessionId = '';

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _sessionId = _generateSessionId();
  }

  String _generateSessionId() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    final rand = Random.secure();
    return List.generate(
      32,
      (index) => chars[rand.nextInt(chars.length)],
    ).join();
  }

  void _sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    setState(() {
      _messages.add({'role': 'user', 'text': text});
      _controller.clear();
      _voiceInput = '';
      _messages.add({'role': 'agent', 'text': '...'});
    });
    _scrollToBottom();

    try {
      final response = await _sendToAgent(text);
      setState(() {
        _messages.removeLast();
        _messages.add({'role': 'agent', 'text': response});
        _controller.clear();
        _voiceInput = '';
      });
      _scrollToBottom();
    } catch (e) {
      setState(() {
        _messages.removeLast();
        _messages.add({
          'role': 'agent',
          'text': 'Error al conectar con el agente.',
        });
        _controller.clear();
        _voiceInput = '';
      });
      _scrollToBottom();
    }
  }

  Future<String> _sendToAgent(String message) async {
    final url = Uri.parse(
      'http://localhost:5678/webhook/53c136fe-3e77-4709-a143-fe82746dd8b6/chat',
    );
    final payload = {
      'sessionId': _sessionId,
      'action': 'sendMessage',
      'chatInput': message,
    };
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload),
      );
      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded.containsKey('output')) {
          return decoded['output'].toString();
        } else {
          return response.body;
        }
      } else {
        throw Exception('Error en el agente: \\${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al conectar con el agente: \\${e.toString()}');
    }
  }

  void _startListening() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) {
            setState(() {
              _voiceInput = val.recognizedWords;
              _controller.text = _voiceInput;
            });
          },
        );
      }
    }
  }

  void _stopListening() {
    if (_isListening) {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _clearChat() {
    setState(() {
      _messages.clear();
      _sessionId = _generateSessionId();
      _controller.clear();
      _voiceInput = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Limpiar chat',
            onPressed: () {
              _clearChat();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isUser = msg['role'] == 'user';
                return Align(
                  alignment:
                      isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.blue[100] : Colors.grey[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child:
                        isUser
                            ? Text(msg['text'] ?? '')
                            : MarkdownBody(
                              data: msg['text'] ?? '',
                              styleSheet: MarkdownStyleSheet(
                                p: const TextStyle(fontSize: 16),
                              ),
                            ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    onSubmitted: _sendMessage,
                    decoration: InputDecoration(
                      hintText: 'Escribe tu mensaje...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: Icon(_isListening ? Icons.mic : Icons.mic_none),
                  color: _isListening ? Colors.red : Colors.blue,
                  onPressed: null,
                ),
                GestureDetector(
                  onLongPressStart: (_) => _startListening(),
                  onLongPressEnd: (_) => _stopListening(),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 100),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: _isListening ? Colors.red : Colors.blue,
                    ),
                    padding: const EdgeInsets.all(8),
                    child: Icon(
                      _isListening ? Icons.mic : Icons.mic_none,
                      color: Colors.white,
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  color: Colors.blue,
                  onPressed: () => _sendMessage(_controller.text),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
